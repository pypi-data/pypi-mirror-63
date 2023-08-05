import itertools
import numpy as np
import time as tm
import os

from .veloxchemlib import ElectronRepulsionIntegralsDriver
from .veloxchemlib import ExcitationVector
from .veloxchemlib import GridDriver
from .veloxchemlib import MolecularGrid
from .veloxchemlib import XCFunctional
from .veloxchemlib import mpi_master
from .veloxchemlib import szblock
from .veloxchemlib import denmat
from .veloxchemlib import rotatory_strength_in_cgs
from .veloxchemlib import parse_xc_func
from .aodensitymatrix import AODensityMatrix
from .lrmatvecdriver import LinearResponseMatrixVectorDriver
from .lrmatvecdriver import remove_linear_dependence_half
from .lrmatvecdriver import orthogonalize_gram_schmidt_half
from .lrmatvecdriver import normalize_half
from .lrmatvecdriver import construct_ed_sd_half
from .lrmatvecdriver import get_rhs
from .lrmatvecdriver import read_rsp_hdf5
from .lrmatvecdriver import write_rsp_hdf5
from .qqscheme import get_qq_scheme
from .qqscheme import get_qq_type
from .errorhandler import assert_msg_critical


class LinearResponseEigenSolver:
    """
    Implements linear response eigensolver.

    :param comm:
        The MPI communicator.
    :param ostream:
        The output stream.

    Instance variables
        - nstates: Number of excited states.
        - eri_thresh: The electron repulsion integrals screening threshold.
        - qq_type: The electron repulsion integrals screening scheme.
        - dft: The flag for running DFT.
        - grid_level: The accuracy level of DFT grid.
        - xcfun: The XC functional.
        - pe: The flag for running polarizable embedding calculation.
        - potfile: The name of the potential file for polarizable embedding.
        - use_split_comm: The flag for using split communicators.
        - conv_thresh: The convergence threshold for the solver.
        - max_iter: The maximum number of solver iterations.
        - cur_iter: Index of the current iteration.
        - small_thresh: The norm threshold for a vector to be considered a zero
          vector.
        - lindep_thresh: The threshold for removing linear dependence in the
          trial vectors.
        - is_converged: The flag for convergence.
        - comm: The MPI communicator.
        - rank: The MPI rank.
        - nodes: Number of MPI processes.
        - ostream: The output stream.
        - restart: The flag for restarting from checkpoint file.
        - checkpoint_file: The name of checkpoint file.
        - checkpoint_time: The timer of checkpoint file.
        - timing: The flag for printing timing information.
        - profiling: The flag for printing profiling information.
    """

    def __init__(self, comm, ostream):
        """
        Initializes linear response eigensolver to default setup.
        """

        # number of states
        self.nstates = 3

        # ERI settings
        self.eri_thresh = 1.0e-15
        self.qq_type = 'QQ_DEN'

        # dft
        self.dft = False
        self.grid_level = 4
        self.xcfun = XCFunctional()

        # polarizable embedding
        self.pe = False
        self.potfile = None

        # split communicators
        self.use_split_comm = False

        # solver setup
        self.conv_thresh = 1.0e-4
        self.max_iter = 50
        self.cur_iter = 0
        self.small_thresh = 1.0e-10
        self.lindep_thresh = 1.0e-6
        self.is_converged = False

        # mpi information
        self.comm = comm
        self.rank = self.comm.Get_rank()
        self.nodes = self.comm.Get_size()

        # output stream
        self.ostream = ostream

        # restart information
        self.restart = True
        self.checkpoint_file = None
        self.checkpoint_time = None

        self.timing = False
        self.timing_dict = None
        self.profiling = False

    def update_settings(self, rsp_dict, method_dict={}):
        """
        Updates response and method settings in linear response eigensolver.

        :param rsp_dict:
            The dictionary of response dict.
        :param method_dict:
            The dictionary of method rsp_dict.
        """

        if 'nstates' in rsp_dict:
            self.nstates = int(rsp_dict['nstates'])

        if 'eri_thresh' in rsp_dict:
            self.eri_thresh = float(rsp_dict['eri_thresh'])
        if 'qq_type' in rsp_dict:
            self.qq_type = str(rsp_dict['qq_type'])

        if 'conv_thresh' in rsp_dict:
            self.conv_thresh = float(rsp_dict['conv_thresh'])
        if 'max_iter' in rsp_dict:
            self.max_iter = int(rsp_dict['max_iter'])
        if 'lindep_thresh' in rsp_dict:
            self.lindep_thresh = float(rsp_dict['lindep_thresh'])

        if 'restart' in rsp_dict:
            key = rsp_dict['restart'].lower()
            self.restart = True if key == 'yes' else False
        if 'checkpoint_file' in rsp_dict:
            self.checkpoint_file = rsp_dict['checkpoint_file']

        if 'timing' in rsp_dict:
            key = rsp_dict['timing'].lower()
            self.timing = True if key in ['yes', 'y'] else False
        if 'profiling' in rsp_dict:
            key = rsp_dict['profiling'].lower()
            self.profiling = True if key in ['yes', 'y'] else False

        if 'dft' in method_dict:
            key = method_dict['dft'].lower()
            self.dft = True if key == 'yes' else False
        if 'grid_level' in method_dict:
            self.grid_level = int(method_dict['grid_level'])
        if 'xcfun' in method_dict:
            if 'dft' not in method_dict:
                self.dft = True
            self.xcfun = parse_xc_func(method_dict['xcfun'].upper())
            assert_msg_critical(not self.xcfun.is_undefined(),
                                'Undefined XC functional')

        if 'pe' in method_dict:
            key = method_dict['pe'].lower()
            self.pe = True if key == 'yes' else False
        if 'potfile' in method_dict:
            if 'pe' not in method_dict:
                self.pe = True
            self.potfile = method_dict['potfile']

        if 'use_split_comm' in method_dict:
            key = method_dict['use_split_comm'].lower()
            self.use_split_comm = True if key == 'yes' else False

    def compute(self, molecule, basis, scf_tensors):
        """
        Performs linear response calculation for a molecule and a basis set.

        :param molecule:
            The molecule.
        :param basis:
            The AO basis set.
        :param scf_tensors:
            The dictionary of tensors from converged SCF wavefunction.

        :return:
            A dictionary containing eigenvalues, eigenvectors, transition
            dipole moments, oscillator strengths and rotatory strengths.
        """

        if self.profiling:
            import cProfile
            import pstats
            import io
            pr = cProfile.Profile()
            pr.enable()

        if self.timing:
            self.timing_dict = {
                'reduced_space': [0.0],
                'ortho_norm': [0.0],
                'fock_build': [0.0],
                'fock_eri': [0.0],
                'fock_dft': [0.0],
                'fock_pe': [0.0],
            }
            timing_t0 = tm.time()

        if self.rank == mpi_master():
            self.print_header()

        self.start_time = tm.time()
        self.checkpoint_time = self.start_time

        # sanity check
        nalpha = molecule.number_of_alpha_electrons()
        nbeta = molecule.number_of_beta_electrons()
        assert_msg_critical(
            nalpha == nbeta,
            'LinearResponseEigenSolver: not implemented for unrestricted case')

        # make preparations
        if self.rank == mpi_master():
            mo = scf_tensors['C']
            ea = scf_tensors['E']
            nocc = nalpha
            norb = mo.shape[1]

        # generate integration grid
        if self.dft:
            grid_drv = GridDriver(self.comm)
            grid_drv.set_level(self.grid_level)

            grid_t0 = tm.time()
            molgrid = grid_drv.generate(molecule)
            n_grid_points = molgrid.number_of_points()
            self.ostream.print_info(
                'Molecular grid with {0:d} points generated in {1:.2f} sec.'.
                format(n_grid_points,
                       tm.time() - grid_t0))
            self.ostream.print_blank()

            if self.rank == mpi_master():
                gs_density = AODensityMatrix([scf_tensors['D'][0]], denmat.rest)
            else:
                gs_density = AODensityMatrix()
            gs_density.broadcast(self.rank, self.comm)

            dft_func_label = self.xcfun.get_func_label().upper()
        else:
            molgrid = MolecularGrid()
            gs_density = AODensityMatrix()
            dft_func_label = 'HF'

        # set up polarizable embedding
        if self.pe:
            from .polembed import PolEmbed
            pe_drv = PolEmbed(molecule, basis, self.comm, self.potfile)
            V_es = pe_drv.compute_multipole_potential_integrals()

            pot_info = "Reading polarizable embedding potential: {}".format(
                self.potfile)
            self.ostream.print_info(pot_info)
            self.ostream.print_blank()

            with open(self.potfile, 'r') as f_pot:
                potfile_text = os.linesep.join(f_pot.readlines())
        else:
            pe_drv = None
            V_es = None
            potfile_text = ''

        # generate screening for ERI

        if self.use_split_comm:
            self.use_split_comm = ((self.dft or self.pe) and self.nodes >= 8)

        if self.use_split_comm:
            screening = None
            valstr = 'ERI'
            if self.dft:
                valstr += '/DFT'
            if self.pe:
                valstr += '/PE'
            self.ostream.print_info(
                'Using sub-communicators for {}.'.format(valstr))
            self.ostream.print_blank()
        else:
            eri_drv = ElectronRepulsionIntegralsDriver(self.comm)
            screening = eri_drv.compute(get_qq_scheme(self.qq_type),
                                        self.eri_thresh, molecule, basis)

        e2x_drv = LinearResponseMatrixVectorDriver(self.comm,
                                                   self.use_split_comm)
        e2x_drv.update_settings(self.eri_thresh, self.qq_type, self.dft,
                                self.xcfun, self.pe, self.potfile)
        timing_dict = {}

        rsp_vector_labels = [
            'LR_eigen_bger_half_size',
            'LR_eigen_bung_half_size',
            'LR_eigen_e2bger_half_size',
            'LR_eigen_e2bung_half_size',
        ]

        bger = None
        bung = None
        new_trials_ger = None
        new_trials_ung = None

        # read initial guess from restart file
        if self.restart:
            if self.rank == mpi_master():
                bger, bung, e2bger, e2bung = read_rsp_hdf5(
                    self.checkpoint_file, rsp_vector_labels,
                    molecule.nuclear_repulsion_energy(),
                    molecule.elem_ids_to_numpy(), basis.get_label(),
                    dft_func_label, potfile_text, self.ostream)
                self.restart = (bger is not None and bung is not None and
                                e2bger is not None and e2bung is not None)
            self.restart = self.comm.bcast(self.restart, root=mpi_master())

        # generate initial guess from scratch
        if not self.restart:
            if self.rank == mpi_master():

                igs = self.initial_excitations(self.nstates, ea, nocc, norb)
                bger, bung = self.setup_trials(igs)

                if self.timing:
                    elapsed_time = tm.time() - timing_t0
                    self.timing_dict['ortho_norm'][0] += elapsed_time
                    timing_t0 = tm.time()

                assert_msg_critical(
                    bger.any() or bung.any(),
                    'LinearResponseEigenSolver: trial vector is empty')

                if bger is None or not bger.any():
                    bger = np.zeros((bung.shape[0], 0))
                if bung is None or not bung.any():
                    bung = np.zeros((bger.shape[0], 0))

            e2bger, e2bung = e2x_drv.e2n_half_size(bger, bung, scf_tensors,
                                                   screening, molecule, basis,
                                                   molgrid, gs_density, V_es,
                                                   pe_drv, timing_dict)

        excitations = [None] * self.nstates
        exresiduals = [None] * self.nstates
        relative_residual_norm = {}
        converged = {}

        if self.timing:
            self.timing_dict['fock_build'][0] += tm.time() - timing_t0
            self.timing_dict['fock_eri'][0] += timing_dict['ERI']
            if self.dft:
                self.timing_dict['fock_dft'][0] += timing_dict['DFT']
            if self.pe:
                self.timing_dict['fock_pe'][0] += timing_dict['PE']
            timing_t0 = tm.time()

        # start iterations
        for iteration in range(self.max_iter):

            if self.timing:
                self.timing_dict['reduced_space'].append(0.0)
                self.timing_dict['ortho_norm'].append(0.0)
                self.timing_dict['fock_build'].append(0.0)
                self.timing_dict['fock_eri'].append(0.0)
                self.timing_dict['fock_dft'].append(0.0)
                self.timing_dict['fock_pe'].append(0.0)

            if self.rank == mpi_master():
                self.cur_iter = iteration
                ws = []

                e2gg = np.matmul(bger.T, e2bger) * 2.0
                e2uu = np.matmul(bung.T, e2bung) * 2.0
                s2ug = np.matmul(bung.T, bger) * 4.0

                # Equations:
                # E[2] X_g - w S[2] X_u = 0
                # E[2] X_u - w S[2] X_g = 0

                # Solutions:
                # (S_gu (E_uu)^-1 S_ug) X_g = 1/w^2 E_gg X_g
                # X_u = w (E_uu)^-1 S_ug X_g

                evals, evecs = np.linalg.eigh(e2uu)
                e2uu_inv = np.linalg.multi_dot(
                    [evecs, np.diag(1.0 / evals), evecs.T])
                ses = np.linalg.multi_dot([s2ug.T, e2uu_inv, s2ug])

                evals, evecs = np.linalg.eigh(e2gg)
                tmat = np.linalg.multi_dot(
                    [evecs, np.diag(1.0 / np.sqrt(evals)), evecs.T])
                ses_tilde = np.linalg.multi_dot([tmat.T, ses, tmat])

                evals, evecs = np.linalg.eigh(ses_tilde)
                p = list(reversed(evals.argsort()))
                evals = evals[p]
                evecs = evecs[:, p]

                wn = 1.0 / np.sqrt(evals[:self.nstates])
                Xn_ger = np.matmul(tmat, evecs[:, :self.nstates])
                Xn_ung = wn * np.linalg.multi_dot([e2uu_inv, s2ug, Xn_ger])

                for k in range(self.nstates):
                    x_ger = Xn_ger[:, k]
                    x_ung = Xn_ung[:, k]
                    norm = np.sqrt(
                        np.linalg.multi_dot([x_ung.T, s2ug, x_ger]) +
                        np.linalg.multi_dot([x_ger.T, s2ug.T, x_ung]))
                    Xn_ger[:, k] /= norm
                    Xn_ung[:, k] /= norm

                for k in range(self.nstates):

                    w = wn[k]
                    c_ger = Xn_ger[:, k]
                    c_ung = Xn_ung[:, k]

                    r_ger = np.matmul(e2bger,
                                      c_ger) - w * 2.0 * np.matmul(bung, c_ung)
                    r_ung = np.matmul(e2bung,
                                      c_ung) - w * 2.0 * np.matmul(bger, c_ger)

                    r = np.array([r_ger, r_ung]).flatten()

                    x_ger = np.matmul(bger, c_ger)
                    x_ung = np.matmul(bung, c_ung)

                    x_ger_full = np.hstack((x_ger, x_ger))
                    x_ung_full = np.hstack((x_ung, -x_ung))

                    X = x_ger_full + x_ung_full

                    exresiduals[k] = (w, r)
                    excitations[k] = (w, X)

                    rn = np.linalg.norm(r) * np.sqrt(2.0)
                    xn = np.linalg.norm(X)
                    relative_residual_norm[k] = rn / xn

                    converged[k] = (rn / xn < self.conv_thresh)
                    ws.append(w)

                # write to output
                self.ostream.print_info(
                    '{:d} gerade trial vectors in reduced space'.format(
                        bger.shape[1]))
                self.ostream.print_info(
                    '{:d} ungerade trial vectors in reduced space'.format(
                        bung.shape[1]))
                self.ostream.print_blank()

                self.print_iteration(relative_residual_norm, converged, ws)

            if self.timing:
                tid = iteration + 1
                self.timing_dict['reduced_space'][tid] += tm.time() - timing_t0
                timing_t0 = tm.time()

            # check convergence
            self.check_convergence(relative_residual_norm)

            if self.is_converged:
                break

            # update trial vectors
            if self.rank == mpi_master():
                precond = [
                    self.get_precond(ea, nocc, norb, w) for w, x in excitations
                ]

                new_trials_ger, new_trials_ung = self.setup_trials(
                    exresiduals, converged, precond, bger, bung)

                assert_msg_critical(
                    new_trials_ger.any() or new_trials_ung.any(),
                    'LinearResponseEigenSolver: unable to add new trial vector')

                if new_trials_ger is None or not new_trials_ger.any():
                    new_trials_ger = np.zeros((new_trials_ung.shape[0], 0))
                if new_trials_ung is None or not new_trials_ung.any():
                    new_trials_ung = np.zeros((new_trials_ger.shape[0], 0))

                bger = np.append(bger, new_trials_ger, axis=1)
                bung = np.append(bung, new_trials_ung, axis=1)

            if self.timing:
                tid = iteration + 1
                self.timing_dict['ortho_norm'][tid] += tm.time() - timing_t0
                timing_t0 = tm.time()

            new_e2bger, new_e2bung = e2x_drv.e2n_half_size(
                new_trials_ger, new_trials_ung, scf_tensors, screening,
                molecule, basis, molgrid, gs_density, V_es, pe_drv, timing_dict)

            if self.rank == mpi_master():
                e2bger = np.append(e2bger, new_e2bger, axis=1)
                e2bung = np.append(e2bung, new_e2bung, axis=1)

                if tm.time() - self.checkpoint_time > 900.0:
                    write_rsp_hdf5(self.checkpoint_file,
                                   [bger, bung, e2bger, e2bung],
                                   rsp_vector_labels,
                                   molecule.nuclear_repulsion_energy(),
                                   molecule.elem_ids_to_numpy(),
                                   basis.get_label(), dft_func_label,
                                   potfile_text, self.ostream)
                    self.checkpoint_time = tm.time()

            if self.timing:
                tid = iteration + 1
                self.timing_dict['fock_build'][tid] += tm.time() - timing_t0
                self.timing_dict['fock_eri'][tid] += timing_dict['ERI']
                if self.dft:
                    self.timing_dict['fock_dft'][tid] += timing_dict['DFT']
                if self.pe:
                    self.timing_dict['fock_pe'][tid] += timing_dict['PE']
                timing_t0 = tm.time()

        # converged?
        if self.rank == mpi_master():
            self.print_convergence()

            assert_msg_critical(
                self.is_converged,
                'LinearResponseEigenSolver.compute: failed to converge')

            if self.timing:
                self.print_timing()

        if self.profiling:
            pr.disable()
            s = io.StringIO()
            sortby = 'cumulative'
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            ps.print_stats(20)
            if self.rank == mpi_master():
                for line in s.getvalue().split(os.linesep):
                    self.ostream.print_info(line)

        dipole_rhs = get_rhs('dipole', 'xyz', molecule, basis, scf_tensors,
                             self.rank, self.comm)
        linmom_rhs = get_rhs('linear_momentum', 'xyz', molecule, basis,
                             scf_tensors, self.rank, self.comm)
        angmom_rhs = get_rhs('angular_momentum', 'xyz', molecule, basis,
                             scf_tensors, self.rank, self.comm)

        if self.rank == mpi_master():
            V_dipole = {op: V for op, V in zip('xyz', dipole_rhs)}
            V_linmom = {op: V for op, V in zip('xyz', linmom_rhs)}
            V_angmom = {op: V for op, V in zip('xyz', angmom_rhs)}

            elec_tms = {}
            velo_tms = {}
            magn_tms = {}

            eigvals = np.array([s[0] for s in excitations])
            eigvecs = [s[1] for s in excitations]

            for comp in 'xyz':
                elec_tms[comp] = np.array(
                    [np.dot(V_dipole[comp], vec) for vec in eigvecs])
                velo_tms[comp] = -1.0 / eigvals * np.array(
                    [np.dot(V_linmom[comp], vec) for vec in eigvecs])
                magn_tms[comp] = 0.5 * np.array(
                    [np.dot(V_angmom[comp], vec) for vec in eigvecs])

            elec_trans_dipoles = [
                np.array([elec_tms['x'][s], elec_tms['y'][s], elec_tms['z'][s]])
                for s in range(self.nstates)
            ]

            velo_trans_dipoles = [
                np.array([velo_tms['x'][s], velo_tms['y'][s], velo_tms['z'][s]])
                for s in range(self.nstates)
            ]

            magn_trans_dipoles = [
                np.array([magn_tms['x'][s], magn_tms['y'][s], magn_tms['z'][s]])
                for s in range(self.nstates)
            ]

            osc = 2.0 / 3.0 * eigvals * (elec_tms['x']**2 + elec_tms['y']**2 +
                                         elec_tms['z']**2)

            rot_vel = (velo_tms['x'] * magn_tms['x'] +
                       velo_tms['y'] * magn_tms['y'] +
                       velo_tms['z'] * magn_tms['z'])

            rot_vel *= rotatory_strength_in_cgs()

            return {
                'eigenvalues': eigvals,
                'eigenvectors': np.array(eigvecs).T,
                'electric_transition_dipoles': elec_trans_dipoles,
                'velocity_transition_dipoles': velo_trans_dipoles,
                'magnetic_transition_dipoles': magn_trans_dipoles,
                'oscillator_strengths': osc,
                'rotatory_strengths': rot_vel,
            }
        else:
            return {}

    def print_header(self):
        """
        Prints linear response eigensolver setup header to output stream.
        """

        self.ostream.print_blank()
        self.ostream.print_header("Linear Response EigenSolver Setup")
        self.ostream.print_header(35 * "=")
        self.ostream.print_blank()

        str_width = 60

        cur_str = "Number of States                : " + str(self.nstates)
        self.ostream.print_header(cur_str.ljust(str_width))

        cur_str = "Max. Number of Iterations       : " + str(self.max_iter)
        self.ostream.print_header(cur_str.ljust(str_width))
        cur_str = "Convergence Threshold           : " + \
            "{:.1e}".format(self.conv_thresh)
        self.ostream.print_header(cur_str.ljust(str_width))

        cur_str = "ERI Screening Scheme            : " + get_qq_type(
            self.qq_type)
        self.ostream.print_header(cur_str.ljust(str_width))
        cur_str = "ERI Screening Threshold         : " + \
            "{:.1e}".format(self.eri_thresh)
        self.ostream.print_header(cur_str.ljust(str_width))

        if self.dft:
            cur_str = "Exchange-Correlation Functional : "
            cur_str += self.xcfun.get_func_label().upper()
            self.ostream.print_header(cur_str.ljust(str_width))
            cur_str = "Molecular Grid Level            : " + str(
                self.grid_level)
            self.ostream.print_header(cur_str.ljust(str_width))

        self.ostream.print_blank()
        self.ostream.flush()

    def print_iteration(self, relative_residual_norm, converged, ws):
        """
        Prints information of the iteration.

        :param relative_residual_norm:
            Relative residual norms.
        :param converged:
            Flags of converged excitations.
        :param ws:
            Excitation energies.
        """

        width = 92
        output_header = '*** Iteration:   {} '.format(self.cur_iter + 1)
        output_header += '* Residuals (Max,Min): '
        output_header += '{:.2e} and {:.2e}'.format(
            max(relative_residual_norm.values()),
            min(relative_residual_norm.values()))
        self.ostream.print_header(output_header.ljust(width))
        self.ostream.print_blank()
        for k, w in enumerate(ws):
            state_label = 'Excitation {}'.format(k + 1)
            rel_res = relative_residual_norm[k]
            output_iter = '{:<15s}: {:15.8f} '.format(state_label, w)
            output_iter += 'Residual Norm: {:.8f}'.format(rel_res)
            if converged[k]:
                output_iter += '   converged'
            self.ostream.print_header(output_iter.ljust(width))
        self.ostream.print_blank()
        self.ostream.flush()

    def print_convergence(self):
        """
        Prints information after convergence.
        """

        width = 92
        output_conv = '*** '
        if self.is_converged:
            output_conv += 'Linear response converged'
        else:
            output_conv += 'Linear response NOT converged'
        output_conv += ' in {:d} iterations. '.format(self.cur_iter + 1)
        output_conv += 'Time: {:.2f} sec'.format(tm.time() - self.start_time)
        self.ostream.print_header(output_conv.ljust(width))
        self.ostream.print_blank()

    def check_convergence(self, relative_residual_norm):
        """
        Checks convergence.

        :param relative_residual_norm:
            Relative residual norms.
        """

        if self.rank == mpi_master():
            max_residual = max(relative_residual_norm.values())
            if max_residual < self.conv_thresh:
                self.is_converged = True

        self.is_converged = self.comm.bcast(self.is_converged,
                                            root=mpi_master())

    def initial_excitations(self, nstates, ea, nocc, norb):
        """
        Gets initial guess for excitations.

        :param nstates:
            Number of excited states.
        :param ea:
            Orbital energies.
        :param nocc:
            Number of occupied orbitals.
        :param norb:
            Number of orbitals.

        :return:
            A list of initial excitations (excitation energy and vector).
        """

        xv = ExcitationVector(szblock.aa, 0, nocc, nocc, norb, True)
        excitations = list(
            itertools.product(xv.bra_unique_indexes(), xv.ket_unique_indexes()))

        excitation_energies = [ea[a] - ea[i] for i, a in excitations]

        w = {ia: w for ia, w in zip(excitations, excitation_energies)}

        final = []
        for (i, a) in sorted(w, key=w.get)[:nstates]:
            ia = excitations.index((i, a))
            n_exc = len(excitations)

            Xn = np.zeros(2 * n_exc)
            Xn[ia] = 1.0

            Xn_T = np.zeros(2 * n_exc)
            Xn_T[:n_exc] = Xn[n_exc:]
            Xn_T[n_exc:] = Xn[:n_exc]

            Xn_ger = 0.5 * (Xn + Xn_T)[:n_exc]
            Xn_ung = 0.5 * (Xn - Xn_T)[:n_exc]

            final.append((w[(i, a)], np.array([Xn_ger, Xn_ung]).flatten()))
        return final

    def setup_trials(self,
                     excitations,
                     converged={},
                     precond=None,
                     bger=None,
                     bung=None,
                     renormalize=True):
        """
        Computes orthonormalized trial vectors.

        :param excitations:
            The set of excitations.
        :param converged:
            The flags of converged excitations.
        :param precond:
            The preconditioner.
        :param bger:
            The gerade subspace.
        :param bung:
            The ungerade subspace.
        :param renormalize:
            The flag for normalization.

        :return:
            The orthonormalized gerade and ungerade trial vectors.
        """

        trials = []

        for k, (w, X) in enumerate(excitations):
            if converged and converged[k]:
                continue

            if precond is not None:
                v = self.preconditioning(precond[k], X)
            else:
                v = X

            if np.linalg.norm(v) * np.sqrt(2.0) > self.small_thresh:
                trials.append(v)

        new_trials = np.array(trials).T

        # decomposing the full space trial vectors...

        new_ger, new_ung = self.decomp_trials(new_trials)

        if bger is not None and bger.any():
            new_ger_proj = np.matmul(bger, 2.0 * np.matmul(bger.T, new_ger))
            new_ger = new_ger - new_ger_proj

        if bung is not None and bung.any():
            new_ung_proj = np.matmul(bung, 2.0 * np.matmul(bung.T, new_ung))
            new_ung = new_ung - new_ung_proj

        if new_ger.any() and renormalize:
            new_ger = remove_linear_dependence_half(new_ger, self.lindep_thresh)
            new_ger = orthogonalize_gram_schmidt_half(new_ger)
            new_ger = normalize_half(new_ger)

        if new_ung.any() and renormalize:
            new_ung = remove_linear_dependence_half(new_ung, self.lindep_thresh)
            new_ung = orthogonalize_gram_schmidt_half(new_ung)
            new_ung = normalize_half(new_ung)

        return new_ger, new_ung

    def get_precond(self, orb_ene, nocc, norb, w):
        """
        Constructs the preconditioner matrix.

        :param orb_ene:
            The orbital energies.
        :param nocc:
            The number of doubly occupied orbitals.
        :param norb:
            The number of orbitals.
        :param w:
            The frequency.

        :return:
            The preconditioner matrix.
        """

        # spawning needed components

        ediag, sdiag = construct_ed_sd_half(orb_ene, nocc, norb)

        ediag_sq = ediag**2
        sdiag_sq = sdiag**2
        w_sq = w**2

        # constructing matrix block diagonals

        pa_diag = ediag / (ediag_sq - w_sq * sdiag_sq)
        pb_diag = (w * sdiag) / (ediag_sq - w_sq * sdiag_sq)

        precond = np.array([pa_diag, pb_diag])

        return precond

    def preconditioning(self, precond, v_in):
        """
        Creates trial vectors out of residuals and the preconditioner matrix.

        :param precond:
            The preconditioner matrix.
        :param v_in:
            The input trial vectors.

        :return:
            The trail vectors after preconditioning.
        """

        pa, pb = precond[0], precond[1]

        v_in_rg, v_in_ru = self.decomp_trials(v_in)

        v_out_rg = pa * v_in_rg + pb * v_in_ru
        v_out_ru = pb * v_in_rg + pa * v_in_ru

        v_out = np.array([v_out_rg, v_out_ru]).flatten()

        return v_out

    def decomp_trials(self, vecs):
        """
        Decomposes trial vectors into gerade and ungerade parts.

        :param vecs:
            The trial vectors.

        :return:
            A tuple containing gerade and ungerade parts of the trial vectors.
        """

        assert_msg_critical(vecs.shape[0] % 2 == 0,
                            'decomp_trials: shape[0] of array should be even')

        ger, ung = None, None
        half_rows = vecs.shape[0] // 2

        if len(vecs.shape) == 1:
            ger = vecs[:half_rows]
            ung = vecs[half_rows:]

        elif len(vecs.shape) == 2:
            ger = vecs[:half_rows, :]
            ung = vecs[half_rows:, :]

        return ger, ung

    def print_timing(self):
        """
        Prints timing for the linear response eigensolver.
        """

        width = 92

        valstr = 'Timing (in sec):'
        self.ostream.print_header(valstr.ljust(width))
        self.ostream.print_header(('-' * len(valstr)).ljust(width))

        valstr = '{:<15s} {:>15s} {:>15s} {:>15s}'.format(
            '', 'ReducedSpace', 'Orthonorm.', 'FockBuild')
        valstr += ' {:>10s}'.format('FockERI')
        if self.dft:
            valstr += ' {:>10s}'.format('FockDFT')
        if self.pe:
            valstr += ' {:>10s}'.format('FockPE')
        self.ostream.print_header(valstr.ljust(width))

        for i, (a, b, c) in enumerate(
                zip(self.timing_dict['reduced_space'],
                    self.timing_dict['ortho_norm'],
                    self.timing_dict['fock_build'])):
            if i == 0:
                title = 'Initial guess'
            else:
                title = 'Iteration {:<5d}'.format(i)
            valstr = '{:<15s} {:15.3f} {:15.3f} {:15.3f}'.format(title, a, b, c)
            valstr += ' {:10.2f}'.format(self.timing_dict['fock_eri'][i])
            if self.dft:
                valstr += ' {:10.2f}'.format(self.timing_dict['fock_dft'][i])
            if self.pe:
                valstr += ' {:10.2f}'.format(self.timing_dict['fock_pe'][i])
            self.ostream.print_header(valstr.ljust(width))

        valstr = '---------'
        self.ostream.print_header(valstr.ljust(width))

        valstr = '{:<15s} {:15.3f} {:15.3f} {:15.3f}'.format(
            'Sum', sum(self.timing_dict['reduced_space']),
            sum(self.timing_dict['ortho_norm']),
            sum(self.timing_dict['fock_build']))
        valstr += ' {:10.2f}'.format(sum(self.timing_dict['fock_eri']))
        if self.dft:
            valstr += ' {:10.2f}'.format(sum(self.timing_dict['fock_dft']))
        if self.pe:
            valstr += ' {:10.2f}'.format(sum(self.timing_dict['fock_pe']))
        self.ostream.print_header(valstr.ljust(width))

        self.ostream.print_blank()

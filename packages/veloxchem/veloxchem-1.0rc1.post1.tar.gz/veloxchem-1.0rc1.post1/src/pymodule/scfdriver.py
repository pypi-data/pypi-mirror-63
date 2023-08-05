from collections import deque
import numpy as np
import time as tm
import math
import os

from .veloxchemlib import OverlapIntegralsDriver
from .veloxchemlib import KineticEnergyIntegralsDriver
from .veloxchemlib import NuclearPotentialIntegralsDriver
from .veloxchemlib import ElectronRepulsionIntegralsDriver
from .veloxchemlib import GridDriver
from .veloxchemlib import MolecularGrid
from .veloxchemlib import XCIntegrator
from .veloxchemlib import AOKohnShamMatrix
from .veloxchemlib import DenseMatrix
from .veloxchemlib import mpi_master
from .veloxchemlib import parse_xc_func
from .veloxchemlib import molorb
from .molecularbasis import MolecularBasis
from .aofockmatrix import AOFockMatrix
from .aodensitymatrix import AODensityMatrix
from .molecularorbitals import MolecularOrbitals
from .subcommunicators import SubCommunicators
from .denguess import DensityGuess
from .qqscheme import get_qq_type
from .qqscheme import get_qq_scheme
from .errorhandler import assert_msg_critical


class ScfDriver:
    """
    Implements SCF method with C2-DIIS and two-level C2-DIIS convergence
    accelerators.

    :param comm:
        The MPI communicator.
    :param ostream:
        The output stream.

    Instance variables
        - den_guess: The initial density guess driver.
        - acc_type: The type of SCF convergence accelerator.
        - max_err_vecs: The maximum number of error vectors.
        - max_iter: The maximum number of SCF iterations.
        - first_step: The flag for first step in two-level C2-DIIS convergence
          acceleration.
        - qq_type: The electron repulsion integrals screening scheme.
        - qq_dyn: The flag for enabling dynamic thresholds in electron
          repulsion integrals screening scheme.
        - conv_thresh: The SCF convergence threshold.
        - eri_thresh: The electron repulsion integrals screening threshold.
        - ovl_thresh: The atomic orbitals linear dependency threshold.
        - diis_thresh: The C2-DIIS switch on threshold.
        - use_level_shift: The flag for usage of level shifting in SCF
          iterations.
        - iter_data: The list of SCF iteration data (electronic energy,
          electronic energy change, gradient, density change).
        - is_converged: The flag for SCF convergence.
        - skip_iter: The flag for SCF iteration data storage.
        - old_energy: The electronic energy of previous SCF iteration.
        - num_iter: The current number of SCF iterations.
        - fock_matrices: The list of stored Fock/Kohn-Sham matrices.
        - den_matrices: The list of stored density matrices.
        - density: The current density matrix.
        - mol_orbs: The current molecular orbitals.
        - nuc_energy: The nuclear repulsion energy of molecule.
        - comm: The MPI communicator.
        - rank: The rank of MPI process.
        - nodes: The number of MPI processes.
        - restart: The flag for restarting from checkpoint file.
        - checkpoint_file: The name of checkpoint file.
        - checkpoint_time: The timer of checkpoint file.
        - ref_mol_orbs: The reference molecular orbitals read from checkpoint
          file.
        - restricted: The flag for restricted SCF.
        - dft: The flag for running DFT.
        - grid_level: The accuracy level of DFT grid.
        - xcfun: The XC functional.
        - molgrid: The molecular grid.
        - pe: The flag for running polarizable embedding calculation.
        - V_es: The polarizable embedding matrix.
        - potfile: The name of the potential file for polarizable embedding.
        - pe_summary: The summary string for polarizable embedding.
        - use_split_comm: The flag for using split communicators.
        - split_comm_ratio: The list of ratios for split communicators.
        - timing: The flag for printing timing information.
        - profiling: The flag for printing profiling information.
    """

    def __init__(self, comm, ostream):
        """
        Initializes SCF driver to default setup (convergence threshold, initial
        guess, etc).
        """

        # scf accelerator
        self.acc_type = "L2_DIIS"
        self.max_err_vecs = 10
        self.max_iter = 50
        self.first_step = False

        # screening scheme
        self.qq_type = "QQ_DEN"
        self.qq_dyn = True

        # thresholds
        self.conv_thresh = 1.0e-6
        self.ovl_thresh = 1.0e-6
        self.diis_thresh = 1000.0
        self.eri_thresh = 1.0e-12
        self.eri_thresh_tight = 1.0e-15

        # level shifting
        self.use_level_shift = False

        # iterations data
        self.iter_data = []
        self.is_converged = False
        self.skip_iter = False
        self.old_energy = 0.0
        self.num_iter = 0

        # DIIS data lists
        self.fock_matrices = deque()
        self.den_matrices = deque()

        self.fock_matrices_beta = deque()
        self.den_matrices_beta = deque()

        # density matrix
        self.density = AODensityMatrix()

        # molecular orbitals
        self.mol_orbs = MolecularOrbitals()

        # nuclear repulsion energy
        self.nuc_energy = 0.0

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
        self.ref_mol_orbs = None

        # restricted?
        self.restricted = True

        # dft
        self.dft = False
        self.grid_level = 4
        self.xcfun = None
        self.molgrid = None

        # polarizable embedding
        self.pe = False
        self.V_es = None
        self.potfile = None
        self.pe_summary = ''

        # split communicators
        self.use_split_comm = False
        self.split_comm_ratio = None

        # timing and profiling
        self.timing = False
        self.profiling = False

    def update_settings(self, scf_dict, method_dict={}):
        """
        Updates settings in SCF driver.

        :param scf_dict:
            The input dictionary of scf group.
        :param method_dict:
            The input dicitonary of method settings group.
        """

        if 'acc_type' in scf_dict:
            self.acc_type = scf_dict['acc_type'].upper()
        if 'max_iter' in scf_dict:
            self.max_iter = int(scf_dict['max_iter'])
        if 'conv_thresh' in scf_dict:
            self.conv_thresh = float(scf_dict['conv_thresh'])
        if 'diis_thresh' in scf_dict:
            self.diis_thresh = float(scf_dict['diis_thresh'])
        if 'qq_type' in scf_dict:
            self.qq_type = scf_dict['qq_type'].upper()
        if 'eri_thresh' in scf_dict:
            self.eri_thresh = float(scf_dict['eri_thresh'])
        if 'restart' in scf_dict:
            key = scf_dict['restart'].lower()
            self.restart = True if key == 'yes' else False
        if 'checkpoint_file' in scf_dict:
            self.checkpoint_file = scf_dict['checkpoint_file']

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

        if 'timing' in scf_dict:
            key = scf_dict['timing'].lower()
            self.timing = True if key in ['yes', 'y'] else False
        if 'profiling' in scf_dict:
            key = scf_dict['profiling'].lower()
            self.profiling = True if key in ['yes', 'y'] else False

    def compute(self, molecule, ao_basis, min_basis=None):
        """
        Performs SCF calculation using molecular data.

        :param molecule:
            The molecule.
        :param ao_basis:
            The AO basis set.
        :param min_basis:
            The minimal AO basis set.
        """

        if min_basis is None:
            if self.rank == mpi_master():
                min_basis = MolecularBasis.read(molecule, 'MIN-CC-PVDZ')
            min_basis.broadcast(self.rank, self.comm)

        # set up timing data
        if self.timing:
            self.timing_dict = {
                'fock_2e': [],
                'dft_vxc': [],
                'fock_diag': [],
                'pol_embed': []
            }

        # check dft setup
        if self.dft:
            assert_msg_critical(self.xcfun is not None,
                                'SCF driver: undefined XC functional')

        # initial guess
        if self.restart:
            self.den_guess = DensityGuess("RESTART", self.checkpoint_file)
            self.restart = self.den_guess.validate_checkpoint(
                self.rank, self.comm, molecule.elem_ids_to_numpy(),
                ao_basis.get_label(), self.restricted)

        if self.restart:
            self.acc_type = "DIIS"
            if self.rank == mpi_master():
                self.ref_mol_orbs = MolecularOrbitals.read_hdf5(
                    self.checkpoint_file)
        else:
            self.den_guess = DensityGuess("SAD")

        # nuclear repulsion energy
        self.nuc_energy = molecule.nuclear_repulsion_energy()

        if self.rank == mpi_master():
            self.print_header()
            valstr = "Nuclear repulsion energy: {:.10f} au".format(
                self.nuc_energy)
            self.ostream.print_info(valstr)
            self.ostream.print_blank()

        # generate integration grid
        if self.dft:
            grid_drv = GridDriver(self.comm)
            grid_drv.set_level(self.grid_level)

            grid_t0 = tm.time()
            self.molgrid = grid_drv.generate(molecule)
            n_grid_points = self.molgrid.number_of_points()
            self.ostream.print_info(
                'Molecular grid with {0:d} points generated in {1:.2f} sec.'.
                format(n_grid_points,
                       tm.time() - grid_t0))
            self.ostream.print_blank()

        # set up polarizable embedding
        if self.pe:
            from .polembed import PolEmbed
            self.pe_drv = PolEmbed(molecule, ao_basis, self.comm, self.potfile)
            self.V_es = self.pe_drv.compute_multipole_potential_integrals()

            pot_info = "Reading polarizable embedding potential: {}".format(
                self.potfile)
            self.ostream.print_info(pot_info)
            self.ostream.print_blank()

        # C2-DIIS method
        if self.acc_type == "DIIS":
            self.comp_diis(molecule, ao_basis, min_basis)

        # two level C2-DIIS method
        if self.acc_type == "L2_DIIS":

            # first step
            self.first_step = True

            old_thresh = self.conv_thresh
            self.conv_thresh = 1.0e-3

            old_max_iter = self.max_iter
            self.max_iter = 5

            val_basis = ao_basis.get_valence_basis()
            self.comp_diis(molecule, val_basis, min_basis)

            # second step
            self.first_step = False

            self.diis_thresh = 1000.0
            self.conv_thresh = old_thresh
            self.max_iter = old_max_iter
            self.den_guess.guess_type = "PRCMO"

            self.comp_diis(molecule, ao_basis, val_basis)

        self.fock_matrices.clear()
        self.den_matrices.clear()

        self.fock_matrices_beta.clear()
        self.den_matrices_beta.clear()

        if self.rank == mpi_master():
            self.print_scf_energy()
            if self.restricted:
                s2 = 0.0
            else:
                s2 = self.compute_s2(molecule, self.scf_tensors['S'],
                                     self.mol_orbs)
            self.print_ground_state(molecule, s2)
            self.mol_orbs.print_orbitals(molecule, ao_basis, False,
                                         self.ostream)

            if (self.checkpoint_file and
                    isinstance(self.checkpoint_file, str) and
                    os.path.isfile(self.checkpoint_file)):
                checkpoint_text = "Checkpoint written to file: "
                checkpoint_text += self.checkpoint_file
                self.ostream.print_info(checkpoint_text)
                self.ostream.print_blank()

            if self.timing:
                self.print_timing()

    def write_checkpoint(self, nuclear_charges, basis_set):
        """
        Writes molecular orbitals to checkpoint file.

        :param nuclear_charges:
            The nuclear charges.
        :param basis_set:
            Name of the basis set.
        """

        if self.rank == mpi_master() and not self.first_step:
            if self.checkpoint_file and isinstance(self.checkpoint_file, str):
                self.mol_orbs.write_hdf5(self.checkpoint_file, nuclear_charges,
                                         basis_set)

    def comp_diis(self, molecule, ao_basis, min_basis):
        """
        Performs SCF calculation with C2-DIIS acceleration.

        :param molecule:
            The molecule.
        :param ao_basis:
            The AO basis set.
        :param min_basis:
            The minimal AO basis set.
        """

        if self.profiling and not self.first_step:
            import cProfile
            import pstats
            import io
            pr = cProfile.Profile()
            pr.enable()

        start_time = tm.time()
        self.checkpoint_time = start_time

        self.fock_matrices.clear()
        self.den_matrices.clear()

        self.fock_matrices_beta.clear()
        self.den_matrices_beta.clear()

        ovl_mat, kin_mat, npot_mat = self.comp_one_ints(molecule, ao_basis)

        linear_dependency = False

        if self.rank == mpi_master():
            t0 = tm.time()

            oao_mat = ovl_mat.get_ortho_matrix(self.ovl_thresh)

            self.ostream.print_info("Orthogonalization matrix computed in" +
                                    " {:.2f} sec.".format(tm.time() - t0))
            self.ostream.print_blank()

            nrow = oao_mat.number_of_rows()
            ncol = oao_mat.number_of_columns()
            linear_dependency = (nrow != ncol)

            if linear_dependency:
                ndim = nrow - ncol
                self.ostream.print_info(
                    "Removed " + str(ndim) + " linearly dependent" +
                    " vector{:s}.".format('' if ndim == 1 else 's'))
                self.ostream.print_blank()
            self.ostream.flush()

        else:
            oao_mat = None

        linear_dependency = self.comm.bcast(linear_dependency,
                                            root=mpi_master())

        if (linear_dependency and self.eri_thresh > self.eri_thresh_tight):
            self.eri_thresh = self.eri_thresh_tight

            if self.rank == mpi_master():
                self.ostream.print_info("ERI screening threshold tightened to" +
                                        " {:.1e}.".format(self.eri_thresh))
                self.ostream.print_blank()

        den_mat = self.comp_guess_density(molecule, ao_basis, min_basis,
                                          ovl_mat)

        den_mat.broadcast(self.rank, self.comm)

        self.density = AODensityMatrix(den_mat)

        fock_mat = AOFockMatrix(den_mat)

        if self.dft and not self.first_step:
            self.update_fock_type(fock_mat)

        if self.use_split_comm:
            self.use_split_comm = ((self.dft or self.pe) and self.nodes >= 8)

        if self.use_split_comm and not self.first_step:
            qq_data = None
            if not self.first_step:
                valstr = 'ERI'
                if self.dft:
                    valstr += '/DFT'
                if self.pe:
                    valstr += '/PE'
                self.ostream.print_info(
                    'Using sub-communicators for {}.'.format(valstr))
        else:
            eri_drv = ElectronRepulsionIntegralsDriver(self.comm)
            qq_data = eri_drv.compute(get_qq_scheme(self.qq_type),
                                      self.eri_thresh, molecule, ao_basis)

        self.split_comm_ratio = None

        e_grad = None

        if self.rank == mpi_master():
            self.print_scf_title()

        for i in self.get_scf_range():

            vxc_mat, e_pe, V_pe = self.comp_2e_fock(fock_mat, den_mat, molecule,
                                                    ao_basis, qq_data, e_grad)

            e_ee, e_kin, e_en = self.comp_energy(fock_mat, vxc_mat, e_pe,
                                                 kin_mat, npot_mat, den_mat)

            self.comp_full_fock(fock_mat, vxc_mat, V_pe, kin_mat, npot_mat)

            e_grad = self.comp_gradient(fock_mat, ovl_mat, den_mat, oao_mat)

            self.set_skip_iter_flag(i, e_grad)

            diff_den = self.comp_density_change(den_mat, self.density)

            self.add_iter_data(e_ee, e_kin, e_en, e_grad, diff_den)

            self.check_convergence()

            self.print_iter_data(i)

            self.store_diis_data(i, fock_mat, den_mat)

            if self.timing and not self.first_step:
                diag_t0 = tm.time()

            eff_fock_mat = self.get_effective_fock(fock_mat, ovl_mat, oao_mat)

            self.mol_orbs = self.gen_molecular_orbitals(eff_fock_mat, oao_mat)

            self.update_mol_orbs_phase()

            if self.timing and not self.first_step:
                self.timing_dict['fock_diag'].append(tm.time() - diag_t0)

            if tm.time() - self.checkpoint_time > 900.0:
                self.write_checkpoint(molecule.elem_ids_to_numpy(),
                                      ao_basis.get_label())
                self.checkpoint_time = tm.time()

            self.density = AODensityMatrix(den_mat)

            den_mat = self.gen_new_density(molecule)

            den_mat.broadcast(self.rank, self.comm)

            if self.is_converged:
                break

        self.write_checkpoint(molecule.elem_ids_to_numpy(),
                              ao_basis.get_label())

        if self.profiling and not self.first_step:
            pr.disable()
            s = io.StringIO()
            sortby = 'cumulative'
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            ps.print_stats(20)
            if self.rank == mpi_master():
                self.ostream.print_blank()
                for line in s.getvalue().split(os.linesep):
                    self.ostream.print_info(line)

        if self.rank == mpi_master():
            self.scf_tensors = {
                'C': self.mol_orbs.alpha_to_numpy(),
                'E': self.mol_orbs.ea_to_numpy(),
                'S': ovl_mat.to_numpy(),
                'D': (self.density.alpha_to_numpy(0),
                      self.density.beta_to_numpy(0)),
                'F': (fock_mat.alpha_to_numpy(0), fock_mat.beta_to_numpy(0)),
            }
        else:
            self.scf_tensors = {
                'C': None,
                'E': None,
                'S': None,
                'D': None,
                'F': None,
            }

        if self.rank == mpi_master():
            self.print_scf_finish(start_time)

        if self.rank == mpi_master() and not self.first_step:
            assert_msg_critical(self.is_converged,
                                'ScfDriver.compute: failed to converge')

    def comp_one_ints(self, molecule, basis):
        """
        Computes one-electron integrals (overlap, kinetic energy and nuclear
        potential) using molecular data.

        :param molecule:
            The molecule.
        :param ao_basis:
            The AO basis set.

        :return:
            The one-electron integrals.
        """

        t0 = tm.time()

        ovl_drv = OverlapIntegralsDriver(self.comm)
        ovl_mat = ovl_drv.compute(molecule, basis)

        t1 = tm.time()

        kin_drv = KineticEnergyIntegralsDriver(self.comm)
        kin_mat = kin_drv.compute(molecule, basis)

        t2 = tm.time()

        if molecule.number_of_atoms() >= self.nodes and self.nodes > 1:
            npot_mat = self.comp_npot_mat_split_comm(molecule, basis)
        else:
            npot_drv = NuclearPotentialIntegralsDriver(self.comm)
            npot_mat = npot_drv.compute(molecule, basis)

        t3 = tm.time()

        if self.rank == mpi_master():

            self.ostream.print_info("Overlap matrix computed in" +
                                    " {:.2f} sec.".format(t1 - t0))
            self.ostream.print_blank()

            self.ostream.print_info("Kinetic energy matrix computed in" +
                                    " {:.2f} sec.".format(t2 - t1))
            self.ostream.print_blank()

            self.ostream.print_info("Nuclear potential matrix computed in" +
                                    " {:.2f} sec.".format(t3 - t2))
            self.ostream.print_blank()

            self.ostream.flush()

        return ovl_mat, kin_mat, npot_mat

    def comp_npot_mat_split_comm(self, molecule, basis):
        """
        Computes one-electron nuclear potential integral on split
        communicators.

        :param molecule:
            The molecule.
        :param ao_basis:
            The AO basis set.

        :return:
            The one-electron nuclear potential matrix.
        """

        node_grps = [p for p in range(self.nodes)]
        subcomm = SubCommunicators(self.comm, node_grps)
        local_comm = subcomm.local_comm
        cross_comm = subcomm.cross_comm

        ave, res = divmod(molecule.number_of_atoms(), self.nodes)
        counts = [ave + 1 if p < res else ave for p in range(self.nodes)]

        start = sum(counts[:self.rank])
        end = sum(counts[:self.rank + 1])

        charges = molecule.elem_ids_to_numpy()[start:end].astype(float)
        coords = np.vstack(
            (molecule.x_to_numpy()[start:end], molecule.y_to_numpy()[start:end],
             molecule.z_to_numpy()[start:end])).T

        npot_drv = NuclearPotentialIntegralsDriver(local_comm)
        npot_mat = npot_drv.compute(molecule, basis, charges, coords)

        if local_comm.Get_rank() == mpi_master():
            npot_mat.reduce_sum(cross_comm.Get_rank(), cross_comm.Get_size(),
                                cross_comm)

        return npot_mat

    def comp_guess_density(self, molecule, ao_basis, min_basis, ovl_mat):
        """
        Computes initial density guess for SCF using superposition of atomic
        densities or molecular orbitals projection methods.

        :param molecule:
            The molecule.
        :param ao_basis:
            The AO basis set.
        :param min_basis:
            The minimal AO basis set.
        :param ovl_mat:
            The overlap matrix between minimal and full AO basis.

        :return:
            The density matrix.
        """

        # guess: read from checkpoint file
        if self.den_guess.guess_type == "RESTART":

            return self.den_guess.restart_density(molecule, self.rank,
                                                  self.ostream)

        # guess: superposition of atomic densities
        if self.den_guess.guess_type == "SAD":

            return self.den_guess.sad_density(molecule, ao_basis, min_basis,
                                              ovl_mat, self.restricted,
                                              self.comm, self.ostream)

        # guess: projection of molecular orbitals from reduced basis
        if self.den_guess.guess_type == "PRCMO":

            if self.rank == mpi_master():
                return self.den_guess.prcmo_density(molecule, ao_basis,
                                                    min_basis, self.mol_orbs)
            else:
                return AODensityMatrix()

        return AODensityMatrix()

    def set_skip_iter_flag(self, i, e_grad):
        """
        Sets SCF iteration skiping flag based on iteration number and C2-DIIS
        switch on threshold.

        :param i:
            The number of current SCF iteration.
        :param e_grad:
            The electronic gradient at current SCF iteration.
        """

        self.num_iter = i

        self.use_level_shift = False

        if e_grad < self.diis_thresh:
            self.skip_iter = False
        else:
            self.skip_iter = True

    def comp_2e_fock(self,
                     fock_mat,
                     den_mat,
                     molecule,
                     basis,
                     screening,
                     e_grad=None):
        """
        Computes Fock/Kohn-Sham matrix (only 2e part).

        :param fock_mat:
            The AO Fock matrix (only 2e-part).
        :param den_mat:
            The AO density matrix.
        :param molecule:
            The molecule.
        :param basis:
            The basis set.
        :param screening:
            The screening container object.
        :param e_grad:
            The electronic gradient.

        :return:
            The AO Kohn-Sham (Vxc) matrix.
        """

        if self.use_split_comm and not self.first_step:
            vxc_mat, e_pe, V_pe = self.comp_2e_fock_split_comm(
                fock_mat, den_mat, molecule, basis, screening, e_grad)

        else:
            vxc_mat, e_pe, V_pe = self.comp_2e_fock_single_comm(
                fock_mat, den_mat, molecule, basis, screening, e_grad)

        return vxc_mat, e_pe, V_pe

    def comp_2e_fock_single_comm(self,
                                 fock_mat,
                                 den_mat,
                                 molecule,
                                 basis,
                                 screening,
                                 e_grad=None):
        """
        Computes Fock/Kohn-Sham matrix on single communicator.

        :param fock_mat:
            The AO Fock matrix (only 2e-part).
        :param den_mat:
            The AO density matrix.
        :param molecule:
            The molecule.
        :param basis:
            The basis set.
        :param screening:
            The screening container object.
        :param e_grad:
            The electronic gradient.

        :return:
            The AO Kohn-Sham (Vxc) matrix.
        """

        if self.qq_dyn and e_grad is not None:
            screening.set_threshold(self.get_dyn_threshold(e_grad))

        eri_drv = ElectronRepulsionIntegralsDriver(self.comm)
        xc_drv = XCIntegrator(self.comm)

        if self.timing and not self.first_step:
            eri_t0 = tm.time()

        eri_drv.compute(fock_mat, den_mat, molecule, basis, screening)
        fock_mat.reduce_sum(self.rank, self.nodes, self.comm)

        if self.timing and not self.first_step:
            self.timing_dict['fock_2e'].append(tm.time() - eri_t0)
            vxc_t0 = tm.time()

        if self.dft and not self.first_step:
            if not self.xcfun.is_hybrid():
                fock_mat.scale(2.0, 0)

            self.molgrid.distribute(self.rank, self.nodes, self.comm)
            vxc_mat = xc_drv.integrate(den_mat, molecule, basis, self.molgrid,
                                       self.xcfun.get_func_label())
            vxc_mat.reduce_sum(self.rank, self.nodes, self.comm)
        else:
            vxc_mat = None

        if self.timing and not self.first_step:
            self.timing_dict['dft_vxc'].append(tm.time() - vxc_t0)
            pe_t0 = tm.time()

        if self.pe and not self.first_step:
            self.pe_drv.V_es = self.V_es.copy()
            dm = den_mat.alpha_to_numpy(0) + den_mat.beta_to_numpy(0)
            e_pe, V_pe = self.pe_drv.get_pe_contribution(dm)
            self.pe_summary = self.pe_drv.cppe_state.summary_string
        else:
            e_pe, V_pe = 0.0, None

        if self.timing and not self.first_step:
            self.timing_dict['pol_embed'].append(tm.time() - pe_t0)

        return vxc_mat, e_pe, V_pe

    def comp_2e_fock_split_comm(self,
                                fock_mat,
                                den_mat,
                                molecule,
                                basis,
                                screening,
                                e_grad=None):
        """
        Computes Fock/Kohn-Sham matrix on split communicators.

        :param fock_mat:
            The AO Fock matrix (only 2e-part).
        :param den_mat:
            The AO density matrix.
        :param molecule:
            The molecule.
        :param basis:
            The basis set.
        :param screening:
            The screening container object.
        :param e_grad:
            The electronic gradient.

        :return:
            The AO Kohn-Sham (Vxc) matrix.
        """

        if self.split_comm_ratio is None:
            if self.dft and self.pe:
                self.split_comm_ratio = [0.34, 0.33, 0.33]
            elif self.dft:
                self.split_comm_ratio = [0.5, 0.5, 0.0]
            elif self.pe:
                self.split_comm_ratio = [0.5, 0.0, 0.5]
            else:
                self.split_comm_ratio = [1.0, 0.0, 0.0]

        if self.dft:
            dft_nodes = int(float(self.nodes) * self.split_comm_ratio[1] + 0.5)
            dft_nodes = max(1, dft_nodes)
        else:
            dft_nodes = 0

        if self.pe:
            pe_nodes = int(float(self.nodes) * self.split_comm_ratio[2] + 0.5)
            pe_nodes = max(1, pe_nodes)
        else:
            pe_nodes = 0

        eri_nodes = max(1, self.nodes - dft_nodes - pe_nodes)

        if eri_nodes == max(eri_nodes, dft_nodes, pe_nodes):
            eri_nodes = self.nodes - dft_nodes - pe_nodes
        elif dft_nodes == max(eri_nodes, dft_nodes, pe_nodes):
            dft_nodes = self.nodes - eri_nodes - pe_nodes
        else:
            pe_nodes = self.nodes - eri_nodes - dft_nodes

        node_grps = [0] * eri_nodes + [1] * dft_nodes + [2] * pe_nodes
        eri_comm = (node_grps[self.rank] == 0)
        dft_comm = (node_grps[self.rank] == 1)
        pe_comm = (node_grps[self.rank] == 2)

        subcomms = SubCommunicators(self.comm, node_grps)
        local_comm = subcomms.local_comm
        cross_comm = subcomms.cross_comm

        # reset molecular grid for DFT and V_es for PE
        if self.rank != mpi_master():
            self.molgrid = MolecularGrid()
            self.V_es = np.zeros(0)
        if self.dft:
            if local_comm.Get_rank() == mpi_master():
                self.molgrid.broadcast(cross_comm.Get_rank(), cross_comm)
        if self.pe:
            if local_comm.Get_rank() == mpi_master():
                self.V_es = cross_comm.bcast(self.V_es, root=mpi_master())

        t0 = tm.time()

        # calculate Fock on ERI nodes
        if eri_comm:
            eri_drv = ElectronRepulsionIntegralsDriver(local_comm)
            local_screening = eri_drv.compute(get_qq_scheme(self.qq_type),
                                              self.eri_thresh, molecule, basis)
            if self.qq_dyn and e_grad is not None:
                local_screening.set_threshold(self.get_dyn_threshold(e_grad))
            eri_drv.compute(fock_mat, den_mat, molecule, basis, local_screening)
            fock_mat.reduce_sum(local_comm.Get_rank(), local_comm.Get_size(),
                                local_comm)
            if self.dft and (not self.xcfun.is_hybrid()):
                fock_mat.scale(2.0, 0)

        # calculate Vxc on DFT nodes
        if dft_comm:
            xc_drv = XCIntegrator(local_comm)
            self.molgrid.distribute(local_comm.Get_rank(),
                                    local_comm.Get_size(), local_comm)
            vxc_mat = xc_drv.integrate(den_mat, molecule, basis, self.molgrid,
                                       self.xcfun.get_func_label())
            vxc_mat.reduce_sum(local_comm.Get_rank(), local_comm.Get_size(),
                               local_comm)
        else:
            vxc_mat = AOKohnShamMatrix()

        # calculate e_pe and V_pe on PE nodes
        if pe_comm:
            from .polembed import PolEmbed
            self.pe_drv = PolEmbed(molecule, basis, local_comm, self.potfile)
            self.pe_drv.V_es = self.V_es.copy()
            dm = den_mat.alpha_to_numpy(0) + den_mat.beta_to_numpy(0)
            e_pe, V_pe = self.pe_drv.get_pe_contribution(dm)
            self.pe_summary = self.pe_drv.cppe_state.summary_string
        else:
            e_pe, V_pe = 0.0, None
            self.pe_summary = ''

        dt = tm.time() - t0

        # collect Vxc to master node
        if self.dft:
            if local_comm.Get_rank() == mpi_master():
                vxc_mat.collect(cross_comm.Get_rank(), cross_comm.Get_size(),
                                cross_comm, 1)

        # collect PE results to master node
        if self.pe:
            pe_root = 2 if self.dft else 1
            if local_comm.Get_rank() == mpi_master():
                e_pe = cross_comm.bcast(e_pe, root=pe_root)
                V_pe = cross_comm.bcast(V_pe, root=pe_root)
                self.pe_summary = cross_comm.bcast(self.pe_summary,
                                                   root=pe_root)

        if local_comm.Get_rank() == mpi_master():
            dt = cross_comm.gather(dt, root=mpi_master())

        if self.rank == mpi_master():
            time_eri = dt[0] * eri_nodes
            time_dft = 0.0
            if self.dft:
                time_dft = dt[1] * dft_nodes
            time_pe = 0.0
            if self.pe:
                pe_root = 2 if self.dft else 1
                time_pe = dt[pe_root] * pe_nodes
            time_sum = time_eri + time_dft + time_pe
            self.split_comm_ratio = [
                time_eri / time_sum,
                time_dft / time_sum,
                time_pe / time_sum,
            ]
        self.split_comm_ratio = self.comm.bcast(self.split_comm_ratio,
                                                root=mpi_master())

        return vxc_mat, e_pe, V_pe

    def comp_energy(self, fock_mat, vxc_mat, e_pe, kin_mat, npot_mat, den_mat):
        """
        Computes SCF energy components: electronic energy, kinetic energy, and
        nuclear potential energy.

        :param fock_mat:
            The Fock/Kohn-Sham matrix (only 2e-part).
        :param vxc_mat:
            The Vxc matrix.
        :param e_pe:
            The polarizable embedding energy.
        :param kin_mat:
            The kinetic energy matrix.
        :param npot_mat:
            The nuclear potential matrix.
        :param den_mat:
            The density matrix.

        :return:
            The tuple (electronic energy, kinetic energy, nuclear potential
            energy).
        """

        e_ee = 0.0
        e_kin = 0.0
        e_en = 0.0

        if self.rank == mpi_master():
            # electronic, kinetic, nuclear energy
            e_ee = fock_mat.get_energy(0, den_mat, 0)
            e_kin = 2.0 * kin_mat.get_energy(den_mat, 0)
            e_en = -2.0 * npot_mat.get_energy(den_mat, 0)
            if self.dft and not self.first_step:
                e_ee += vxc_mat.get_energy()
            if self.pe and not self.first_step:
                e_ee += e_pe

        e_ee = self.comm.bcast(e_ee, root=mpi_master())
        e_kin = self.comm.bcast(e_kin, root=mpi_master())
        e_en = self.comm.bcast(e_en, root=mpi_master())

        return (e_ee, e_kin, e_en)

    def comp_full_fock(self, fock_mat, vxc_mat, pe_mat, kin_mat, npot_mat):
        """
        Computes full Fock/Kohn-Sham matrix by adding to 2e-part of
        Fock/Kohn-Sham matrix the kinetic energy and nuclear potential
        matrices.

        :param fock_mat:
            The Fock/Kohn-Sham matrix (2e-part).
        :param vxc_mat:
            The Vxc matrix.
        :param pe_mat:
            The polarizable embedding matrix.
        :param kin_mat:
            The kinetic energy matrix.
        :param npot_mat:
            The nuclear potential matrix.
        """

        if self.rank == mpi_master():
            fock_mat.add_hcore(kin_mat, npot_mat, 0)
            if self.dft and not self.first_step:
                fock_mat.add_matrix(vxc_mat.get_matrix(), 0)
            if self.pe and not self.first_step:
                fock_mat.add_matrix(DenseMatrix(pe_mat), 0)

    def comp_gradient(self, fock_mat, ovl_mat, den_mat, oao_mat):
        """
        Computes electronic gradient using Fock/Kohn-Sham matrix.

        :param fock_mat:
            The Fock/Kohn-Sham matrix.
        :param ovl_mat:
            The overlap matrix.
        :param den_mat:
            The density matrix.
        :param oao_mat:
            The orthogonalization matrix.

        :return:
            The electronic gradient.
        """

        return 0.0

    def comp_density_change(self, den_mat, old_den_mat):
        """
        Computes norm of density change between two density matrices.

        :param den_mat:
            The current density matrix.
        :param old_den_mat:
            The previous density matrix.

        :return:
            The norm of change between two density matrices.
        """

        return 0.0

    def store_diis_data(self, i, fock_mat, den_mat):
        """
        Stores Fock/Kohn-Sham and density matrices for current iteration.

        :param i:
            The number of current SCF iteration.
        :param fock_mat:
            The Fock/Kohn-Sham matrix.
        :param den_mat:
            The density matrix.
        """

        return

    def get_effective_fock(self, fock_mat, ovl_mat, oao_mat):
        """
        Computes effective Fock/Kohn-Sham matrix in OAO basis by applying
        Lowdin or canonical orthogonalization to AO Fock/Kohn-Sham matrix.

        :param fock_mat:
            The Fock/Kohn-Sham matrix.
        :param ovl_mat:
            The overlap matrix.
        :param oao_mat:
            The orthogonalization matrix.

        :return:
            The effective Fock/Kohn-Sham matrix.
        """

        return None

    def gen_molecular_orbitals(self, fock_mat, oao_mat):
        """
        Generates molecular orbital by diagonalizing Fock/Kohn-Sham matrix.

        :param fock_mat:
            The Fock/Kohn-Sham matrix.
        :param oao_mat:
            The orthogonalization matrix.

        :return:
            The molecular orbitals.
        """

        return MolecularOrbitals()

    def update_mol_orbs_phase(self):
        """
        Updates phase of molecular orbitals.
        """

        if self.rank == mpi_master():
            if self.ref_mol_orbs is None:
                return

            ref_mo = self.ref_mol_orbs.alpha_to_numpy()
            mo = self.mol_orbs.alpha_to_numpy()
            ea = self.mol_orbs.ea_to_numpy()

            for col in range(mo.shape[1]):
                if np.dot(mo[:, col], ref_mo[:, col]) < 0.0:
                    mo[:, col] *= -1.0

            if self.mol_orbs.get_orbitals_type() == molorb.rest:
                self.mol_orbs = MolecularOrbitals([mo], [ea], molorb.rest)

            elif self.mol_orbs.get_orbitals_type() == molorb.unrest:
                ref_mo_b = self.ref_mol_orbs.beta_to_numpy()
                mo_b = self.mol_orbs.beta_to_numpy()
                eb = self.mol_orbs.eb_to_numpy()

                for col in range(mo_b.shape[1]):
                    if np.dot(mo_b[:, col], ref_mo_b[:, col]) < 0.0:
                        mo_b[:, col] *= -1.0

                self.mol_orbs = MolecularOrbitals([mo, mo_b], [ea, eb],
                                                  molorb.unrest)

    def gen_new_density(self, molecule):
        """
        Generates density matrix from current molecular orbitals.

        :param molecule:
            The molecule.

        :return:
            The density matrix.
        """

        if self.rank == mpi_master():
            return self.mol_orbs.get_density(molecule)

        return AODensityMatrix()

    def get_dyn_threshold(self, e_grad):
        """
        Computes screening threshold for electron repulsion integrals based on
        value of electronic gradient.

        :param e_grad:
            The electronic gradient.

        :return:
            The screening threshold.
        """

        if e_grad < 1.0e-6:
            return self.eri_thresh

        nteri = math.pow(10, math.floor(math.log10(e_grad)))

        nteri = 1.0e-10 * nteri

        if nteri > 1.0e-10:
            return 1.0e-10

        if nteri < self.eri_thresh:
            return self.eri_thresh

        return nteri

    def add_iter_data(self, e_ee, e_kin, e_en, e_grad, diff_den):
        """
        Adds SCF iteration data (electronic energy, electronic energy change,
        electronic gradient, density difference) to SCF iterations list.

        :param e_ee:
            The electronic energy.
        :param e_kin:
            The kinetic energy.
        :param e_en:
            The nuclear potential energy.
        :param e_grad:
            The electronic energy gradient.
        :param diff_den:
            The density change with respect to previous SCF iteration.
        """

        e_elec = e_ee + e_kin + e_en + self.nuc_energy

        de_elec = e_elec - self.old_energy

        self.iter_data.append((e_elec, de_elec, e_grad, diff_den))

        self.old_energy = e_elec

    def check_convergence(self):
        """
        Sets SCF convergence flag by checking if convergence condition for
        electronic gradient is fullfiled.
        """

        self.is_converged = False

        if len(self.iter_data) > 1:

            e_elec, de_elec, e_grad, diff_den = self.iter_data[-1]

            if e_grad < self.conv_thresh:
                self.is_converged = True

    def get_scf_range(self):
        """
        Creates range of SCF iterations from maximum number of SCF iterations.

        :return:
            The range of SCF iterations.
        """

        return range(self.max_iter + 1)

    def print_scf_energy(self):
        """
        Prints SCF energy information to output stream.
        """

        valstr = self.get_scf_type() + ':'
        self.ostream.print_header(valstr.ljust(92))
        self.ostream.print_header(('-' * len(valstr)).ljust(92))
        self.print_energy_components()

        if self.pe:
            self.ostream.print_blank()
            for line in self.pe_summary.split(os.linesep):
                self.ostream.print_header(line.ljust(92))
            self.ostream.flush()

    def print_header(self):
        """
        Prints SCF calculation setup details to output stream,
        """

        self.ostream.print_blank()
        self.ostream.print_header("Self Consistent Field Driver Setup")
        self.ostream.print_header(36 * "=")
        self.ostream.print_blank()

        str_width = 84
        cur_str = "Wave Function Model             : " + self.get_scf_type()
        self.ostream.print_header(cur_str.ljust(str_width))
        cur_str = "Initial Guess Model             : " + self.get_guess_type()
        self.ostream.print_header(cur_str.ljust(str_width))

        cur_str = "Convergence Accelerator         : " + self.get_acc_type()
        self.ostream.print_header(cur_str.ljust(str_width))
        cur_str = "Max. Number of Iterations       : " + str(self.max_iter)
        self.ostream.print_header(cur_str.ljust(str_width))
        cur_str = "Max. Number of Error Vectors    : " + str(self.max_err_vecs)
        self.ostream.print_header(cur_str.ljust(str_width))
        cur_str = "Convergence Threshold           : " + \
            "{:.1e}".format(self.conv_thresh)
        self.ostream.print_header(cur_str.ljust(str_width))

        cur_str = "ERI Screening Scheme            : " + get_qq_type(
            self.qq_type)
        self.ostream.print_header(cur_str.ljust(str_width))
        cur_str = "ERI Screening Mode              : " + self.get_qq_dyn()
        self.ostream.print_header(cur_str.ljust(str_width))
        cur_str = "ERI Screening Threshold         : " + \
            "{:.1e}".format(self.eri_thresh)
        self.ostream.print_header(cur_str.ljust(str_width))
        cur_str = "Linear Dependence Threshold     : " + \
            "{:.1e}".format(self.ovl_thresh)
        self.ostream.print_header(cur_str.ljust(str_width))

        if self.dft:
            cur_str = "Exchange-Correlation Functional : "
            cur_str += self.xcfun.get_func_label().upper()
            self.ostream.print_header(cur_str.ljust(str_width))
            cur_str = "Molecular Grid Level            : " + str(
                self.grid_level)
            self.ostream.print_header(cur_str.ljust(str_width))

        self.ostream.print_blank()

    def print_scf_title(self):
        """
        Prints SCF cycles header to output stream.
        """

        if self.first_step:
            self.ostream.print_info("Starting Reduced Basis SCF calculation...")

        else:
            self.ostream.print_blank()
            if self.dft:
                self.ostream.print_header(
                    "Iter. |     Kohn-Sham Energy, au    | "
                    "Energy Change, au |  Gradient Norm  | "
                    "Density Change |")
            else:
                self.ostream.print_header(
                    "Iter. |   Hartree-Fock Energy, au   | "
                    "Energy Change, au |  Gradient Norm  | "
                    "Density Change |")
            self.ostream.print_header(92 * "-")

    def print_scf_finish(self, start_time):
        """
        Prints SCF calculation finish message to output stream,

        :param start_time:
            The start time of SCF calculation.
        """

        if self.first_step:
            valstr = "...done. SCF energy in reduced basis set: "
            valstr += "{:.12f}".format(self.old_energy)
            valstr += " au. Time: "
            valstr += "{:.2f}".format(tm.time() - start_time) + " sec."
            self.ostream.print_info(valstr)
            self.ostream.print_blank()

        else:
            valstr = "*** SCF "
            if self.is_converged:
                valstr += "converged in "
            else:
                valstr += "NOT converged in "
            valstr += str(self.num_iter)
            valstr += " iterations. Time: "
            valstr += "{:.2f}".format(tm.time() - start_time) + " sec."
            self.ostream.print_blank()
            self.ostream.print_header(valstr.ljust(92))
            self.ostream.print_blank()

        self.ostream.flush()

    def print_iter_data(self, i):
        """
        Prints SCF iteration data to output stream,

        :param i:
            The current SCF iteration.
        """

        if self.rank == mpi_master():
            # no output for first step in two level DIIS
            if self.first_step:
                return

            # DIIS or second step in two level DIIS
            if i > 0:

                if len(self.iter_data) > 0:
                    te, diff_te, e_grad, diff_den = self.iter_data[-1]

                if i == 1:
                    diff_te = 0.0
                    diff_den = 0.0

                exec_str = " " + (str(i)).rjust(3) + 4 * " "
                exec_str += ("{:7.12f}".format(te)).center(27) + 3 * " "
                exec_str += ("{:5.10f}".format(diff_te)).center(17) + 3 * " "
                exec_str += ("{:5.8f}".format(e_grad)).center(15) + 3 * " "
                exec_str += ("{:5.8f}".format(diff_den)).center(15) + " "

                self.ostream.print_header(exec_str)
                self.ostream.flush()

    def get_scf_energy(self):
        """
        Gets SCF energy from previous SCF iteration.

        :return:
            The SCF energy.
        """

        return self.old_energy

    def get_scf_type(self):
        """
        Gets string with type of SCF calculation (defined in derrived classes).

        :return:
            The string with type of SCF calculation.
        """

        return "Undefined"

    def get_guess_type(self):
        """
        Gets string with type of initial guess (superposition of atomic
        densities or projection of molecular orbitals).

        :return:
            The string with type of initial guess.
        """

        if self.den_guess.guess_type == "SAD":
            return "Superposition of Atomic Densities"

        if self.den_guess.guess_type == "RESTART":
            return "Restart from Checkpoint"

        return "Undefined"

    def get_acc_type(self):
        """
        Gets string with type of SCF convergence accelerator (DIIS or two level
        DIIS).

        :return:
            The string with type of SCF convergence accelerator.
        """

        if self.acc_type == "DIIS":
            return "Direct Inversion of Iterative Subspace"

        if self.acc_type == "L2_DIIS":
            return "Two Level Direct Inversion of Iterative Subspace"

        return "Undefined"

    def get_qq_dyn(self):
        """
        Gets string with application method (static or dynamic) of electron
        repulsion integrals screening.

        :return:
            The string with application method of electron repulsion integrals
            screening.
        """

        if self.qq_dyn:
            return "Dynamic"

        return "Static"

    def update_fock_type(self, fock_mat):
        """
        Updates Fock matrix to fit selected functional in Kohn-Sham
        calculations.

        :param fock_mat:
            The Fock/Kohn-Sham matrix.
        """

        return

    def need_min_basis(self):
        """
        Determines if minimal AO basis is needed in SCF calculation. Usage of
        two level DIIS accelerator or superposition of atomic densities initial
        guess requires minimal AO basis.

        :return:
            The flag for need of minimal AO basis.
        """

        if self.acc_type == "L2_DIIS":
            return True

        if self.den_guess.guess_type == "SAD":
            return True

        return False

    def delete_mos(self, mol_orbs, mol_eigs):
        """
        Generates trimmed molecular orbital by deleting MOs with coeficients
        exceeding 1.0 / sqrt(ovl_thresh).

        :param mol_orbs:
            The molecular orbitals.
        :param mol_eigs:
            The eigenvalues of molecular orbitals.

        :return:
            The tuple (trimmed molecular orbitals, eigenvalues).
        """

        fmax = 1.0 / math.sqrt(self.ovl_thresh)

        mvec = np.amax(np.abs(mol_orbs), axis=0)

        molist = []
        for i in range(mvec.shape[0]):
            if mvec[i] < fmax:
                molist.append(i)

        return (mol_orbs[:, molist], mol_eigs[molist])

    def compute_s2(self, molecule, smat, mol_orbs):
        """
        Computes expectation value of the S**2 operator.

        :param molecule:
            The molecule.
        :param smat:
            The overlap matrix (numpy array).
        :param mol_orbs:
            The molecular orbitals.

        :return:
            Expectation value <S**2>.
        """

        return None

    def print_ground_state(self, molecule, s2):
        """
        Prints ground state information to output stream.

        :param molecule:
            The molecule.
        :param s2:
            The expectation value of S**2.
        """

        self.ostream.print_blank()

        self.ostream.print_header("Ground State Information".ljust(92))
        self.ostream.print_header("------------------------".ljust(92))

        chg = molecule.get_charge()
        valstr = "Charge of Molecule            :{:5.1f}".format(chg)
        self.ostream.print_header(valstr.ljust(92))

        mult = molecule.get_multiplicity()
        valstr = "Multiplicity (2S+1)           :{:5.1f}".format(mult)
        self.ostream.print_header(valstr.ljust(92))

        sz = 0.5 * (mult - 1.0)
        valstr = "Magnetic Quantum Number (S_z) :{:5.1f}".format(sz)
        self.ostream.print_header(valstr.ljust(92))

        if not self.restricted:
            valstr = "Expectation value of S**2     :{:8.4f}".format(s2)
            self.ostream.print_header(valstr.ljust(92))

        self.ostream.print_blank()

    def print_energy_components(self):
        """
        Prints SCF energy components to output stream.
        """

        enuc = self.nuc_energy

        etot = self.iter_data[-1][0]

        e_el = etot - enuc

        valstr = "Total Energy                       :{:20.10f} au".format(etot)
        self.ostream.print_header(valstr.ljust(92))

        valstr = "Electronic Energy                  :{:20.10f} au".format(e_el)
        self.ostream.print_header(valstr.ljust(92))

        valstr = "Nuclear Repulsion Energy           :{:20.10f} au".format(enuc)
        self.ostream.print_header(valstr.ljust(92))

        self.ostream.print_header(
            "------------------------------------".ljust(92))

        grad = self.iter_data[-1][2]
        valstr = "Gradient Norm                      :{:20.10f} au".format(grad)
        self.ostream.print_header(valstr.ljust(92))

    def print_timing(self):
        """
        Prints timing breakdown for the scf driver.
        """

        width = 92

        valstr = 'Timing (in sec):'
        self.ostream.print_header(valstr.ljust(width))
        self.ostream.print_header(('-' * len(valstr)).ljust(width))

        valstr = '{:<15s} {:>15s}'.format('', 'Fock 2E Part')
        if self.dft:
            valstr += ' {:>15s}'.format('XC Part')
        if self.pe:
            valstr += ' {:>15s}'.format('PE Part')
        valstr += ' {:>15s}'.format('Diag. Part')
        self.ostream.print_header(valstr.ljust(width))

        for i in range(len(self.timing_dict['fock_2e'])):

            title = 'Iteration {:<5d}'.format(i)
            valstr = '{:<15s} {:15.3f}'.format(title,
                                               self.timing_dict['fock_2e'][i])
            if self.dft:
                valstr += ' {:15.3f}'.format(self.timing_dict['dft_vxc'][i])
            if self.pe:
                valstr += ' {:15.3f}'.format(self.timing_dict['pol_embed'][i])
            valstr += ' {:15.3f}'.format(self.timing_dict['fock_diag'][i])
            self.ostream.print_header(valstr.ljust(width))

        self.ostream.print_blank()

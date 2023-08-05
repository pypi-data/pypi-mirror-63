# mpi4py
try:
    from mpi4py import MPI
except ImportError:
    raise ImportError('Unable to import mpi4py.MPI')

# C++ classes
from .veloxchemlib import AtomBasis
from .veloxchemlib import BasisFunction
from .veloxchemlib import OverlapIntegralsDriver
from .veloxchemlib import KineticEnergyIntegralsDriver
from .veloxchemlib import NuclearPotentialIntegralsDriver
from .veloxchemlib import ElectricDipoleIntegralsDriver
from .veloxchemlib import ElectronRepulsionIntegralsDriver
from .veloxchemlib import SADGuessDriver
from .veloxchemlib import DenseMatrix
from .veloxchemlib import TwoIndexes
from .veloxchemlib import MOIntsBatch
from .veloxchemlib import ExcitationVector

# C++ functions
from .veloxchemlib import mpi_master
from .veloxchemlib import mpi_initialized
from .veloxchemlib import ao_matrix_to_veloxchem
from .veloxchemlib import ao_matrix_to_dalton
from .veloxchemlib import bohr_in_angstroms
from .veloxchemlib import hartree_in_ev
from .veloxchemlib import mathconst_pi

# C++ enums
from .veloxchemlib import denmat
from .veloxchemlib import ericut
from .veloxchemlib import molorb
from .veloxchemlib import moints

# Python classes
from .inputparser import InputParser
from .outputstream import OutputStream
from .molecule import Molecule
from .molecularbasis import MolecularBasis
from .aodensitymatrix import AODensityMatrix
from .molecularorbitals import MolecularOrbitals
from .aofockmatrix import AOFockMatrix
from .scfrestdriver import ScfRestrictedDriver
from .scfunrestdriver import ScfUnrestrictedDriver
from .mointsdriver import MOIntegralsDriver
from .mp2driver import Mp2Driver
from .visualizationdriver import VisualizationDriver
from .excitondriver import ExcitonModelDriver
from .rspdriver import ResponseDriver
from .tdaexcidriver import TDAExciDriver
from .blockdavidson import BlockDavidsonSolver
from .lreigensolver import LinearResponseEigenSolver
from .lrsolver import LinearResponseSolver
from .rspproperty import ResponseProperty
from .rsplinabscross import LinearAbsorptionCrossSection
from .rspcdspec import CircularDichroismSpectrum
from .rsppolarizability import Polarizability
from .rspabsorption import Absorption
from .mpitask import MpiTask
from .subcommunicators import SubCommunicators
from .cppsolver import ComplexResponse
from .c6solver import C6Solver
from .loprop import LoPropDriver

# Python functions
from .errorhandler import assert_msg_critical
from .qqscheme import get_qq_type
from .qqscheme import get_qq_scheme

# Environment variable: basis set path
import os
if 'VLXBASISPATH' not in os.environ:
    module_path = os.path.dirname(os.path.abspath(__file__))
    os.environ['VLXBASISPATH'] = os.path.join(module_path, 'basis')
if 'OMP_NUM_THREADS' not in os.environ:
    import multiprocessing
    import sys
    ncores = multiprocessing.cpu_count()
    os.environ['OMP_NUM_THREADS'] = str(ncores)
    print('* Warning * Environment variable OMP_NUM_THREADS not set.',
          file=sys.stdout)
    print('* Warning * Setting OMP_NUM_THREADS to {:d}.'.format(ncores),
          file=sys.stdout)

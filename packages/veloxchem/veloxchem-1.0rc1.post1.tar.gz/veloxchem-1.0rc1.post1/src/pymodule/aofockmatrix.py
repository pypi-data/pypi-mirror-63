import numpy as np
import h5py

from .veloxchemlib import AOFockMatrix
from .veloxchemlib import fockmat
from .errorhandler import assert_msg_critical


def _AOFockMatrix_write_hdf5(self, fname):
    """
    Writes AOFockMatrix to hdf5 file.

    :param fname:
        The name of the hdf5 file.
    """

    focktype = {
        fockmat.restjk: "restjk",
        fockmat.restjkx: "restjkx",
        fockmat.restj: "restj",
        fockmat.restk: "restk",
        fockmat.restkx: "restkx",
        fockmat.rgenjk: "rgenjk",
        fockmat.rgenjkx: "rgenjkx",
        fockmat.rgenj: "rgenj",
        fockmat.rgenk: "rgenk",
        fockmat.rgenkx: "rgenkx",
    }

    hf = h5py.File(fname, 'w')

    factors = []
    for i in range(self.number_of_fock_matrices()):
        factors.append(self.get_scale_factor(i))
    hf.create_dataset("factors", data=factors, compression="gzip")

    for i in range(self.number_of_fock_matrices()):
        index = self.get_density_identifier(i)
        name = "{}_{}_{}".format(i, focktype[self.get_fock_type(i)], index)
        array = self.to_numpy(i)
        hf.create_dataset(name, data=array, compression="gzip")

    hf.close()


@staticmethod
def _AOFockMatrix_read_hdf5(fname):
    """
    Reads AOFockMatrix from hdf5 file.

    :param fname:
        The name of the hdf5 file.

    :return:
        The AOFockMatrix.
    """

    focktype = {
        "restjk": fockmat.restjk,
        "restjkx": fockmat.restjkx,
        "restj": fockmat.restj,
        "restk": fockmat.restk,
        "restkx": fockmat.restkx,
        "rgenjk": fockmat.rgenjk,
        "rgenjkx": fockmat.rgenjkx,
        "rgenj": fockmat.rgenj,
        "rgenk": fockmat.rgenk,
        "rgenkx": fockmat.rgenkx,
    }

    hf = h5py.File(fname, 'r')

    focks = []
    types = []
    factors = list(hf.get("factors"))
    indices = []

    ordered_keys = []
    for key in list(hf.keys()):
        if key == "factors":
            continue
        i = int(key.split("_")[0])
        ordered_keys.append((i, key))
    ordered_keys.sort()

    for i, key in ordered_keys:
        type_str, index_str = key.split("_")[1:]
        focks.append(np.array(hf.get(key)))
        types.append(focktype[type_str])
        indices.append(int(index_str))

    hf.close()

    for ftype in set(types):
        assert_msg_critical(ftype in list(focktype.values()),
                            "AOFockMatrix.read_hdf5: invalid Fock types!")

    return AOFockMatrix(focks, types, factors, indices)


AOFockMatrix.write_hdf5 = _AOFockMatrix_write_hdf5
AOFockMatrix.read_hdf5 = _AOFockMatrix_read_hdf5

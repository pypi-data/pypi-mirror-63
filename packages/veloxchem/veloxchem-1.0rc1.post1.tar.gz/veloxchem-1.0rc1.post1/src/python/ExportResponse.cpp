//
//                           VELOXCHEM 1.0-RC
//      ---------------------------------------------------
//                     An Electronic Structure Code
//
//  Copyright © 2018-2020 by VeloxChem developers. All rights reserved.
//  Contact: https://veloxchem.org/contact

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <mpi.h>

#include "ExportResponse.hpp"

#include "ExcitationVector.hpp"
#include "ExportGeneral.hpp"
#include "ExportMath.hpp"
#include "ScreeningContainer.hpp"

namespace py = pybind11;

namespace vlx_response {  // vlx_response namespace

// Exports classes/functions in src/response to python

// Helper function for printing CExcitationVector

static std::string
CExcitationVector_str(const CExcitationVector& self)
{
    return self.getString();
}

// Helper function for converting Z vector to numpy array

static py::array_t<double>
CExcitationVector_zvector_to_numpy(const CExcitationVector& self)
{
    return vlx_general::pointer_to_numpy(self.getCoefficientsZ(), self.getNumberOfExcitations(), 1);
}

// Helper function for converting Y vector to numpy array

static py::array_t<double>
CExcitationVector_yvector_to_numpy(const CExcitationVector& self)
{
    return vlx_general::pointer_to_numpy(self.getCoefficientsY(), self.getNumberOfExcitations(), 1);
}

// Helper function for setting Z and Y vectors

static void
CExcitationVector_set_yzcoefficients(CExcitationVector&         self,
                                     const std::vector<double>& z_coef,
                                     const std::vector<double>& y_coef)
{
    CMemBlock<double> zCoefficients(z_coef);

    CMemBlock<double> yCoefficients(y_coef);

    self.setCoefficientsZY(zCoefficients, yCoefficients);
}

// Helper function for converting approximate diagonal of A matrix to numpy array

static py::array_t<double>
CExcitationVector_diagonal_to_numpy(const CExcitationVector& self, const CMolecularOrbitals& molecularOrbitals)
{
    auto diagmat = self.getApproximateDiagonal(molecularOrbitals);

    return vlx_general::pointer_to_numpy(diagmat.data(), diagmat.size(), 1);
}

static py::array_t<int32_t>
CExcitationVector_bra_indexes_to_numpy(const CExcitationVector& self)
{
    return vlx_general::pointer_to_numpy(self.getBraIndexes(), self.getNumberOfExcitations());
}

static py::array_t<int32_t>
CExcitationVector_ket_indexes_to_numpy(const CExcitationVector& self)
{
    return vlx_general::pointer_to_numpy(self.getKetIndexes(), self.getNumberOfExcitations());
}

// Exports classes/functions in src/response to python

void
export_response(py::module& m)
{
    // CExcitationVector class

    py::class_<CExcitationVector, std::shared_ptr<CExcitationVector>>(m, "ExcitationVector")
        .def(py::init<>())
        .def(py::init<const szblock,
                      const std::vector<int32_t>&,
                      const std::vector<int32_t>&,
                      const std::vector<double>&,
                      const std::vector<double>&>())
        .def(py::init<const szblock, const int32_t, const int32_t, const int32_t, const int32_t, const bool>())
        .def(py::init<const szblock, const int32_t, const int32_t, const int32_t, const int32_t>())
        .def(py::init<const std::vector<double>&, const std::vector<CExcitationVector>&>())
        .def(py::init<const CExcitationVector&>())
        .def("__str__", &CExcitationVector_str)
        .def("set_zcoefficient", &CExcitationVector::setCoefficientZ)
        .def("set_ycoefficient", &CExcitationVector::setCoefficientY)
        .def("set_yzcoefficients", &CExcitationVector_set_yzcoefficients)
        .def("number_excitations", &CExcitationVector::getNumberOfExcitations)
        .def("bra_unique_indexes", &CExcitationVector::getBraUniqueIndexes)
        .def("ket_unique_indexes", &CExcitationVector::getKetUniqueIndexes)
        .def("bra_indexes", &CExcitationVector_bra_indexes_to_numpy)
        .def("ket_indexes", &CExcitationVector_ket_indexes_to_numpy)
        .def("get_zmatrix", &CExcitationVector::getMatrixZ)
        .def("get_ymatrix", &CExcitationVector::getMatrixY)
        .def("get_zdensity", &CExcitationVector::getDensityZ)
        .def("get_ydensity", &CExcitationVector::getDensityY)
        .def("small_energy_identifiers", &CExcitationVector::getSmallEnergyIdentifiers)
        .def("zvector_to_numpy", &CExcitationVector_zvector_to_numpy)
        .def("yvector_to_numpy", &CExcitationVector_yvector_to_numpy)
        .def("diagonal_to_numpy", &CExcitationVector_diagonal_to_numpy);
}

}  // namespace vlx_response

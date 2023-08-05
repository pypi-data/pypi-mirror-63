//
//                           VELOXCHEM 1.0-RC
//      ---------------------------------------------------
//                     An Electronic Structure Code
//
//  Copyright © 2018-2020 by VeloxChem developers. All rights reserved.
//  Contact: https://veloxchem.org/contact

#ifndef DensityMatrixType_hpp
#define DensityMatrixType_hpp

#include <string>

/**
 Enumerate class denmat:

 Defines supported density matrix types:
 denmat::rest   - the restricted density matrix
 denmat::unrest - the unrestricted density matrix
 denmat::rmoij  - the restricted C_i C_j^T matrix
 denmat::umoij  - the unrestricted C_i C_j^T matrix
 denmat::rgen   - the general non-symmetric restricted density matrix
 */
enum class denmat
{
    rest,
    unrest,
    rmoij,
    umoij,
    rgen
};

/**
 Converts key value of density matrix type to integer number.

 @param denMatrix the enumerate class value.
 @return the integer number.
 */
inline int32_t
to_int(const denmat denMatrix)
{
    return static_cast<int32_t>(denMatrix);
}

/**
 Converts integer key value to density matrix type.

 @param keyValue the integer key value.
 @return the density matrix type.
 */
inline denmat
to_denmat(const int32_t keyValue)
{
    if (keyValue == to_int(denmat::rest)) return denmat::rest;

    if (keyValue == to_int(denmat::unrest)) return denmat::unrest;

    if (keyValue == to_int(denmat::rmoij)) return denmat::rmoij;

    if (keyValue == to_int(denmat::umoij)) return denmat::umoij;

    if (keyValue == to_int(denmat::rgen)) return denmat::rgen;

    return denmat::rest;
}

/**
 Converts enumerate class value to it's string label.

 @param denMatrix the enumerate class value.
 @return the label of enumerate class value.
 */
inline std::string
to_string(const denmat denMatrix)
{
    if (denMatrix == denmat::rest)
    {
        return std::string("Restricted Density Matrix");
    }

    if (denMatrix == denmat::unrest)
    {
        return std::string("Unrestricted Density Matrix");
    }

    if (denMatrix == denmat::rmoij)
    {
        return std::string("Restricted C_iC_j^T Density Matrix");
    }

    if (denMatrix == denmat::umoij)
    {
        return std::string("Unrestricted C_iC_j^T Density Matrix");
    }

    if (denMatrix == denmat::rgen)
    {
        return std::string("General Non-Symmetric Restricted Density Matrix");
    }

    return std::string("UNKNOWN");
}

#endif /* DensityMatrixType_hpp */

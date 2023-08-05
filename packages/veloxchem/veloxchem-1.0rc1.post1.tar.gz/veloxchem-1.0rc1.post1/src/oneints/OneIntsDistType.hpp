//
//                           VELOXCHEM 1.0-RC
//      ---------------------------------------------------
//                     An Electronic Structure Code
//
//  Copyright © 2018-2020 by VeloxChem developers. All rights reserved.
//  Contact: https://veloxchem.org/contact

#ifndef OneIntsDistType_hpp
#define OneIntsDistType_hpp

#include <string>

/**
 Enumerate class dist1e:

 Defines supported one electron integrals distribution keys:
 dist1e::symsq  - the symmetric square matrix
 dist1e::antisq - the antisymmetric square matrix
 dist1e::rect   - the general rectangular matrix
 dist1e::batch  - the batch with natural order of data
 */
enum class dist1e
{
    symsq,
    antisq,
    rect,
    batch
};

/**
 Converts enumerate class value to it's string label.

 @param distPattern the enumerate class value.
 @return the label of enumerate class value.
 */
inline std::string
to_string(const dist1e distPattern)
{
    if (distPattern == dist1e::symsq)
    {
        return std::string("Symmetric Square Matrix");
    }

    if (distPattern == dist1e::antisq)
    {
        return std::string("Anti-symmetric Square Matrix");
    }

    if (distPattern == dist1e::rect)
    {
        return std::string("Rectangular Matrix");
    }

    if (distPattern == dist1e::batch)
    {
        return std::string("Raw Integrals Batch");
    }

    return std::string("UNKNOWN");
}

#endif /* OneIntsDistType_hpp */

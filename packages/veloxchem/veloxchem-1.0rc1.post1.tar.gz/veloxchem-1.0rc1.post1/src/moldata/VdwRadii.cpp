//
//                           VELOXCHEM 1.0-RC
//      ---------------------------------------------------
//                     An Electronic Structure Code
//
//  Copyright © 2018-2020 by VeloxChem developers. All rights reserved.
//  Contact: https://veloxchem.org/contact

#include "VdwRadii.hpp"

#include <cstring>

#include "Codata.hpp"

namespace vdwradii {  // vdwradii namespace

std::vector<double>
buildVdwRadii()
{
    // VDW radii in Angstrom

    std::vector<double> radii({

        // dummy
        0.00,

        // H-B
        1.09,
        1.40,
        1.82,
        2.00,
        2.00,

        // C-Ne
        1.70,
        1.55,
        1.52,
        1.47,
        1.54,

        // Na-P
        2.27,
        1.73,
        2.00,
        2.10,
        1.80,

        // S-Ca
        1.80,
        1.75,
        1.88,
        2.75,
        2.00,

        // Sc-Mn
        2.00,
        2.00,
        2.00,
        2.00,
        2.00,

        // Fe-Zn
        2.00,
        2.00,
        1.63,
        1.40,
        1.39,

        // Ga-Br
        1.87,
        2.00,
        1.85,
        1.90,
        1.85,

        // Kr-Zr
        2.02,
        2.00,
        2.00,
        2.00,
        2.00,

        // Nb-Rh
        2.00,
        2.00,
        2.00,
        2.00,
        2.00,

        // Pd-Sn
        1.63,
        1.72,
        1.58,
        1.93,
        2.17,

        // Sb-Cs
        2.00,
        2.06,
        1.98,
        2.16,
        2.00,

        // Ba-Nd (no data for La-Nd)
        2.00,
        2.00,
        2.00,
        2.00,
        2.00,

        // Pm-Tb (no data)
        2.00,
        2.00,
        2.00,
        2.00,
        2.00,

        // Dy-Yb (no data)
        2.00,
        2.00,
        2.00,
        2.00,
        2.00,

        // Lu-Re
        2.00,
        2.00,
        2.00,
        2.00,
        2.00,

        // Os-Hg
        2.00,
        2.00,
        1.72,
        1.66,
        1.55,

        // Tl-At
        1.96,
        2.02,
        2.00,
        2.00,
        2.00,

        // Rn
        2.00});

    // VDW radii in Bohr

    for (size_t i = 0; i < radii.size(); i++)
    {
        radii[i] /= units::getBohrValueInAngstroms();
    }

    return radii;
}

}  // namespace vdwradii

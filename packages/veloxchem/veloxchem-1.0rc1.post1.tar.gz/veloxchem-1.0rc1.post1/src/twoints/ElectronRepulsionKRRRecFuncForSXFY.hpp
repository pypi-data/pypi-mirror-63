//
//                           VELOXCHEM 1.0-RC
//      ---------------------------------------------------
//                     An Electronic Structure Code
//
//  Copyright © 2018-2020 by VeloxChem developers. All rights reserved.
//  Contact: https://veloxchem.org/contact

#include<cstdint>

#include "MemBlock2D.hpp"
#include "GtoPairsBlock.hpp"
#include "RecursionMap.hpp"

namespace erikrrfunc { // erikrrfunc namespace

    /**
    Computes batch of contracted (SX|G|FF) electron repulsion integrals and stores
    results in integrals buffer.

    @param ketBuffer the horizontal recursion buffer for ket side.
    @param recursionMap the recursion map object.
    @param cdDistances the vector of distances R(CD) = C - D.
    @param braGtoPairsBlock the GTOs pairs block on ket side.
    @param ketGtoPairsBlock the GTOs pairs block on ket side.
    @param nKetContrPairs the number of contractes GTOs pairs on ket side.
    @param iContrPair the index of contracted GTO pair on bra side.
    */
    void compElectronRepulsionForSXFF(      CMemBlock2D<double>& ketBuffer,
                                      const CRecursionMap&       recursionMap,
                                      const CMemBlock2D<double>& cdDistances,
                                      const CGtoPairsBlock&      braGtoPairsBlock,
                                      const CGtoPairsBlock&      ketGtoPairsBlock,
                                      const int32_t              nKetContrPairs,
                                      const int32_t              iContrPair);

    /**
    Computes batch of contracted (SX|G|FG) electron repulsion integrals and stores
    results in integrals buffer.

    @param ketBuffer the horizontal recursion buffer for ket side.
    @param recursionMap the recursion map object.
    @param cdDistances the vector of distances R(CD) = C - D.
    @param braGtoPairsBlock the GTOs pairs block on ket side.
    @param ketGtoPairsBlock the GTOs pairs block on ket side.
    @param nKetContrPairs the number of contractes GTOs pairs on ket side.
    @param iContrPair the index of contracted GTO pair on bra side.
    */
    void compElectronRepulsionForSXFG(      CMemBlock2D<double>& ketBuffer,
                                      const CRecursionMap&       recursionMap,
                                      const CMemBlock2D<double>& cdDistances,
                                      const CGtoPairsBlock&      braGtoPairsBlock,
                                      const CGtoPairsBlock&      ketGtoPairsBlock,
                                      const int32_t              nKetContrPairs,
                                      const int32_t              iContrPair);

    /**
    Computes sub-batch (0,75) of contracted (SX|G|FG) electron repulsion integrals and stores
    results in integrals buffer.

    @param ketBuffer the horizontal recursion buffer for ket side.
    @param recursionMap the recursion map object.
    @param cdDistances the vector of distances R(CD) = C - D.
    @param braGtoPairsBlock the GTOs pairs block on ket side.
    @param ketGtoPairsBlock the GTOs pairs block on ket side.
    @param nKetContrPairs the number of contractes GTOs pairs on ket side.
    @param iContrPair the index of contracted GTO pair on bra side.
    */
    void compElectronRepulsionForSXFG_0_75(      CMemBlock2D<double>& ketBuffer,
                                           const CRecursionMap&       recursionMap,
                                           const CMemBlock2D<double>& cdDistances,
                                           const CGtoPairsBlock&      braGtoPairsBlock,
                                           const CGtoPairsBlock&      ketGtoPairsBlock,
                                           const int32_t              nKetContrPairs,
                                           const int32_t              iContrPair);

    /**
    Computes sub-batch (75,150) of contracted (SX|G|FG) electron repulsion integrals and stores
    results in integrals buffer.

    @param ketBuffer the horizontal recursion buffer for ket side.
    @param recursionMap the recursion map object.
    @param cdDistances the vector of distances R(CD) = C - D.
    @param braGtoPairsBlock the GTOs pairs block on ket side.
    @param ketGtoPairsBlock the GTOs pairs block on ket side.
    @param nKetContrPairs the number of contractes GTOs pairs on ket side.
    @param iContrPair the index of contracted GTO pair on bra side.
    */
    void compElectronRepulsionForSXFG_75_150(      CMemBlock2D<double>& ketBuffer,
                                             const CRecursionMap&       recursionMap,
                                             const CMemBlock2D<double>& cdDistances,
                                             const CGtoPairsBlock&      braGtoPairsBlock,
                                             const CGtoPairsBlock&      ketGtoPairsBlock,
                                             const int32_t              nKetContrPairs,
                                             const int32_t              iContrPair);

    /**
    Computes batch of contracted (SX|G|FH) electron repulsion integrals and stores
    results in integrals buffer.

    @param ketBuffer the horizontal recursion buffer for ket side.
    @param recursionMap the recursion map object.
    @param cdDistances the vector of distances R(CD) = C - D.
    @param braGtoPairsBlock the GTOs pairs block on ket side.
    @param ketGtoPairsBlock the GTOs pairs block on ket side.
    @param nKetContrPairs the number of contractes GTOs pairs on ket side.
    @param iContrPair the index of contracted GTO pair on bra side.
    */
    void compElectronRepulsionForSXFH(      CMemBlock2D<double>& ketBuffer,
                                      const CRecursionMap&       recursionMap,
                                      const CMemBlock2D<double>& cdDistances,
                                      const CGtoPairsBlock&      braGtoPairsBlock,
                                      const CGtoPairsBlock&      ketGtoPairsBlock,
                                      const int32_t              nKetContrPairs,
                                      const int32_t              iContrPair);

    /**
    Computes sub-batch (0,70) of contracted (SX|G|FH) electron repulsion integrals and stores
    results in integrals buffer.

    @param ketBuffer the horizontal recursion buffer for ket side.
    @param recursionMap the recursion map object.
    @param cdDistances the vector of distances R(CD) = C - D.
    @param braGtoPairsBlock the GTOs pairs block on ket side.
    @param ketGtoPairsBlock the GTOs pairs block on ket side.
    @param nKetContrPairs the number of contractes GTOs pairs on ket side.
    @param iContrPair the index of contracted GTO pair on bra side.
    */
    void compElectronRepulsionForSXFH_0_70(      CMemBlock2D<double>& ketBuffer,
                                           const CRecursionMap&       recursionMap,
                                           const CMemBlock2D<double>& cdDistances,
                                           const CGtoPairsBlock&      braGtoPairsBlock,
                                           const CGtoPairsBlock&      ketGtoPairsBlock,
                                           const int32_t              nKetContrPairs,
                                           const int32_t              iContrPair);

    /**
    Computes sub-batch (70,140) of contracted (SX|G|FH) electron repulsion integrals and stores
    results in integrals buffer.

    @param ketBuffer the horizontal recursion buffer for ket side.
    @param recursionMap the recursion map object.
    @param cdDistances the vector of distances R(CD) = C - D.
    @param braGtoPairsBlock the GTOs pairs block on ket side.
    @param ketGtoPairsBlock the GTOs pairs block on ket side.
    @param nKetContrPairs the number of contractes GTOs pairs on ket side.
    @param iContrPair the index of contracted GTO pair on bra side.
    */
    void compElectronRepulsionForSXFH_70_140(      CMemBlock2D<double>& ketBuffer,
                                             const CRecursionMap&       recursionMap,
                                             const CMemBlock2D<double>& cdDistances,
                                             const CGtoPairsBlock&      braGtoPairsBlock,
                                             const CGtoPairsBlock&      ketGtoPairsBlock,
                                             const int32_t              nKetContrPairs,
                                             const int32_t              iContrPair);

    /**
    Computes sub-batch (140,210) of contracted (SX|G|FH) electron repulsion integrals and stores
    results in integrals buffer.

    @param ketBuffer the horizontal recursion buffer for ket side.
    @param recursionMap the recursion map object.
    @param cdDistances the vector of distances R(CD) = C - D.
    @param braGtoPairsBlock the GTOs pairs block on ket side.
    @param ketGtoPairsBlock the GTOs pairs block on ket side.
    @param nKetContrPairs the number of contractes GTOs pairs on ket side.
    @param iContrPair the index of contracted GTO pair on bra side.
    */
    void compElectronRepulsionForSXFH_140_210(      CMemBlock2D<double>& ketBuffer,
                                              const CRecursionMap&       recursionMap,
                                              const CMemBlock2D<double>& cdDistances,
                                              const CGtoPairsBlock&      braGtoPairsBlock,
                                              const CGtoPairsBlock&      ketGtoPairsBlock,
                                              const int32_t              nKetContrPairs,
                                              const int32_t              iContrPair);


} // erikrrfunc namespace


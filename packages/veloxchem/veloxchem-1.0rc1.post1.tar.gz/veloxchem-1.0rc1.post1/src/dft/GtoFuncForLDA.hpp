//
//                           VELOXCHEM 1.0-RC
//      ---------------------------------------------------
//                     An Electronic Structure Code
//
//  Copyright © 2018-2020 by VeloxChem developers. All rights reserved.
//  Contact: https://veloxchem.org/contact

#ifndef GtoFuncForLDA_hpp
#define GtoFuncForLDA_hpp

#include <cstdint>

#include "GtoContainer.hpp"
#include "MemBlock2D.hpp"

namespace ldarec {  // ldarec namespace
    
    /**
     Computes S-type GTOs values on given grid.

     @param spherGtoGridBuffer the buffer for storing contracted spherical GTOs values on the grid.
     @param gridCoordinatesX the vector of Cartesian X coordinates of grid points.
     @param gridCoordinatesY the vector of Cartesian Y coordinates of grid points.
     @param gridCoordinatesZ the vector of Cartesian Y coordinates of grid points.
     @param gridOffset the batch offset in vector grid points.
     @param gtoBlock the GTOs block.
     @param iContrGto the index of contracted GTO is GTOs block.
     */
    void compGtoValuesForS(      CMemBlock2D<double>& spherGtoGridBuffer,
                           const double*              gridCoordinatesX,
                           const double*              gridCoordinatesY,
                           const double*              gridCoordinatesZ,
                           const int32_t              gridOffset,
                           const CGtoBlock&           gtoBlock,
                           const int32_t              iContrGto);
    
    
    /**
     Computes P-type GTOs values on given grid.
    
    @param spherGtoGridBuffer the buffer for storing contracted spherical GTOs values on the grid.
    @param cartGtoGridBuffer the buffer for storing primitive Cartesian GTOs values on the grid.
    @param gridCoordinatesX the vector of Cartesian X coordinates of grid points.
    @param gridCoordinatesY the vector of Cartesian Y coordinates of grid points.
    @param gridCoordinatesZ the vector of Cartesian Y coordinates of grid points.
    @param gridOffset the batch offset in vector grid points.
    @param gtoBlock the GTOs block.
    @param iContrGto the index of contracted GTO is GTOs block.
    */
    void compGtoValuesForP(      CMemBlock2D<double>& spherGtoGridBuffer,
                                 CMemBlock2D<double>& cartGtoGridBuffer,
                           const double*              gridCoordinatesX,
                           const double*              gridCoordinatesY,
                           const double*              gridCoordinatesZ,
                           const int32_t              gridOffset,
                           const CGtoBlock&           gtoBlock,
                           const int32_t              iContrGto);
    
    /**
     Computes D-type GTOs values on given grid.
     
     @param spherGtoGridBuffer the buffer for storing contracted spherical GTOs values on the grid.
     @param cartGtoGridBuffer the buffer for storing primitive Cartesian GTOs values on the grid.
     @param gridCoordinatesX the vector of Cartesian X coordinates of grid points.
     @param gridCoordinatesY the vector of Cartesian Y coordinates of grid points.
     @param gridCoordinatesZ the vector of Cartesian Y coordinates of grid points.
     @param gridOffset the batch offset in vector grid points.
     @param gtoBlock the GTOs block.
     @param iContrGto the index of contracted GTO is GTOs block.
     */
    void compGtoValuesForD(      CMemBlock2D<double>& spherGtoGridBuffer,
                                 CMemBlock2D<double>& cartGtoGridBuffer,
                           const double*              gridCoordinatesX,
                           const double*              gridCoordinatesY,
                           const double*              gridCoordinatesZ,
                           const int32_t              gridOffset,
                           const CGtoBlock&           gtoBlock,
                           const int32_t              iContrGto);
    
}  // namespace ldarec

#endif /* GtoFuncForLDA_hpp */

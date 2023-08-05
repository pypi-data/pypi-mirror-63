//
//                           VELOXCHEM 1.0-RC
//      ---------------------------------------------------
//                     An Electronic Structure Code
//
//  Copyright © 2018-2020 by VeloxChem developers. All rights reserved.
//  Contact: https://veloxchem.org/contact

#ifndef Becke88Functional_hpp
#define Becke88Functional_hpp

#include "DensityGrid.hpp"
#include "XCGradientGrid.hpp"
#include "XCFunctional.hpp"

namespace vxcfuncs {  // vxcfuncs namespace
    
    /**
     Sets exchange-correlation functional to Becke (1988) functional.
     
     @return the exchange-correlation functional object.
     */
    CXCFunctional setBecke88Functional();
    
    /**
     Sets primitive exchange-correlation functional to Becke (1988) functional.
     
     @return the exchange-correlation functional object.
     */
    CPrimitiveFunctional setPrimitiveBecke88Functional();
    
    /**
     Implements first order derivatives of Becke (1988) functional for dengrid::ab case.
     
     @param xcGradientGrid the exchange-correlation gradient grid.
     @param factor the scale factor of functional contribution.
     @param densityGrid the density grid.
     */
    void Becke88FuncGradientAB(      CXCGradientGrid& xcGradientGrid,
                               const double           factor,
                               const CDensityGrid&    densityGrid);
    
    
    /**
     Implements first order derivatives of Becke (1988) functional for dengrid::lima case.
     
     @param xcGradientGrid the exchange-correlation gradient grid.
     @param factor the scale factor of functional contribution.
     @param densityGrid the density grid.
     */
    void Becke88FuncGradientA(      CXCGradientGrid& xcGradientGrid,
                              const double           factor,
                              const CDensityGrid&    densityGrid);
    
    /**
     Implements first order derivatives of Becke (1988) functional for dengrid::lima case.
     
     @param xcGradientGrid the exchange-correlation gradient grid.
     @param factor the scale factor of functional contribution.
     @param densityGrid the density grid.
     */
    void Becke88FuncGradientB(      CXCGradientGrid& xcGradientGrid,
                              const double           factor,
                              const CDensityGrid&    densityGrid);
    
    
    /**
     Implements second order derivatives of spin-polarized Becke (1988) functional for dengrid::ab case.
     
     @param xcHessianGrid the exchange-correlation hessian grid.
     @param factor the scale factor of functional contribution.
     @param densityGrid the density grid.
     */
    void Becke88FuncHessianAB(      CXCHessianGrid& xcHessianGrid,
                              const double         factor,
                              const CDensityGrid&  densityGrid);
    
    /**
     Implements second order derivatives of spin-polarized Becke (1988) functional for dengrid::lima case.
     
     @param xcHessianGrid the exchange-correlation hessian grid.
     @param factor the scale factor of functional contribution.
     @param densityGrid the density grid.
     */
    void Becke88FuncHessianA(      CXCHessianGrid& xcHessianGrid,
                             const double          factor,
                             const CDensityGrid&   densityGrid);
    
    /**
     Implements second order derivatives of spin-polarized Becke (1988) functional for dengrid::lima case.
     
     @param xcHessianGrid the exchange-correlation hessian grid.
     @param factor the scale factor of functional contribution.
     @param densityGrid the density grid.
     */
    void Becke88FuncHessianB(      CXCHessianGrid& xcHessianGrid,
                             const double          factor,
                             const CDensityGrid&   densityGrid);
    
}  // namespace vxcfuncs

#endif /* Becke88Functional_hpp */

//
//                           VELOXCHEM 1.0-RC
//      ---------------------------------------------------
//                     An Electronic Structure Code
//
//  Copyright © 2018-2020 by VeloxChem developers. All rights reserved.
//  Contact: https://veloxchem.org/contact

#include "VWN3Functional.hpp"

#include <cmath>

#include "MathConst.hpp"

namespace vxcfuncs {  // vxcfuncs namespace
    
    CXCFunctional
    setVWN3Functional()
    {
        return CXCFunctional({"VWN3"}, xcfun::lda, 0.0, {setPrimitiveVWN3Functional()}, {1.0});
    }
    
    CPrimitiveFunctional
    setPrimitiveVWN3Functional()
    {
        return CPrimitiveFunctional({"VWN3"}, xcfun::lda,
                                    &vxcfuncs::VWN3FuncGradientAB,
                                    &vxcfuncs::VWN3FuncGradientA,
                                    &vxcfuncs::VWN3FuncGradientB,
                                    &vxcfuncs::VWN3FuncHessianAB,
                                    &vxcfuncs::VWN3FuncHessianA,
                                    &vxcfuncs::VWN3FuncHessianB);
    }
    
    void
    VWN3FuncGradientAB(      CXCGradientGrid& xcGradientGrid,
                       const double           factor,
                       const CDensityGrid&    densityGrid)
    {
        // paramagnetic fitting factors
        
        double pa = 0.0621814, pb = 13.0720, pc = 42.7198, px0 = -0.4092860;
        
        double pq = std::sqrt(4.0 * pc - pb * pb);
        
        double pxf0 = px0 * px0 + pb * px0 + pc;
        
        double pyf0 = pq / (pb + 2.0 * px0);
        
        double b = px0 / pxf0;
        
        double c = pxf0 * pyf0;
        
        double acon= b * pb - 1.0;
        
        double bcon = 2.0 * acon + 2.0;
        
        double ccon = 2.0 * pb * (1.0 / pq - px0 / c);
        
        // various prefactor
        
        double f16 = -1.0 / 6.0;
        
        double f76 = -7.0 / 6.0;
        
        double dcrs = std::pow(3.0 / (4.0 * mathconst::getPiValue()), -f16);
        
        double fpre = factor * 0.5 * pa;
        
        // determine number of grid points
        
        auto ngpoints = densityGrid.getNumberOfGridPoints();
        
        // set up pointers to density grid data
        
        auto rhoa = densityGrid.alphaDensity(0);
        
        auto rhob = densityGrid.betaDensity(0);
        
        // set up pointers to functional data
        
        auto fexc = xcGradientGrid.xcFunctionalValues();
        
        auto grhoa = xcGradientGrid.xcGradientValues(xcvars::rhoa);
        
        auto grhob = xcGradientGrid.xcGradientValues(xcvars::rhob);
        
        // diamagnetic contribution
        
        #pragma omp simd aligned(rhoa, rhob, fexc, grhoa, grhob: VLX_ALIGN)
        for (int32_t i = 0; i < ngpoints; i++)
        {
            double rho = rhoa[i] + rhob[i];
            
            double x = dcrs * std::pow(rho, f16);
            
            double xrho  = dcrs * f16 * std::pow(rho, f76);
            
            double xf = x * x + pb * x + pc;
            
            double xfx = 2.0 * x + pb;
            
            double yf = pq / xfx;
            
            double fpe1 = 2.0 * std::log(x) + acon * std::log(xf) - bcon * std::log(x - px0) + ccon * std::atan(yf);
            
            double fpex1 = 2.0 / x + acon * xfx / xf - bcon / (x - px0) - ccon * (2.0 * yf / xfx) / (1.0 + yf * yf);
            
            fexc[i] += fpre * fpe1 * rho;
            
            grhoa[i] += fpre * (fpe1 + rho * fpex1 * xrho);
            
            grhob[i] += fpre * (fpe1 + rho * fpex1 * xrho);
        }
    }
    
    void
    VWN3FuncGradientA(      CXCGradientGrid& xcGradientGrid,
                      const double           factor,
                      const CDensityGrid&    densityGrid)
    {
        // paramagnetic fitting factors
        
        double pa = 0.0621814, pb = 13.0720, pc = 42.7198, px0 = -0.4092860;
        
        double pq = std::sqrt(4.0 * pc - pb * pb);
        
        double pxf0 = px0 * px0 + pb * px0 + pc;
        
        double pyf0 = pq / (pb + 2.0 * px0);
        
        double b = px0 / pxf0;
        
        double c = pxf0 * pyf0;
        
        double acon= b * pb - 1.0;
        
        double bcon = 2.0 * acon + 2.0;
        
        double ccon = 2.0 * pb * (1.0 / pq - px0 / c);
        
        // various prefactor
        
        double f16 = -1.0 / 6.0;
        
        double f76 = -7.0 / 6.0;
        
        double dcrs = std::pow(3.0 / (4.0 * mathconst::getPiValue()), -f16);
        
        double fpre = factor * 0.5 * pa;
        
        // determine number of grid points
        
        auto ngpoints = densityGrid.getNumberOfGridPoints();
        
        // set up pointers to density grid data
        
        auto rhob = densityGrid.betaDensity(0);
        
        // set up pointers to functional data
        
        auto fexc = xcGradientGrid.xcFunctionalValues();
        
        auto grhob = xcGradientGrid.xcGradientValues(xcvars::rhob);
        
        // diamagnetic contribution
        
        #pragma omp simd aligned(rhob, fexc, grhob: VLX_ALIGN)
        for (int32_t i = 0; i < ngpoints; i++)
        {
            double rho = rhob[i];
            
            double x = dcrs * std::pow(rho, f16);
            
            double xrho  = dcrs * f16 * std::pow(rho, f76);
            
            double xf = x * x + pb * x + pc;
            
            double xfx = 2.0 * x + pb;
            
            double yf = pq / xfx;
            
            double fpe1 = 2.0 * std::log(x) + acon * std::log(xf) - bcon * std::log(x - px0) + ccon * std::atan(yf);
            
            double fpex1 = 2.0 / x + acon * xfx / xf - bcon / (x - px0) - ccon * (2.0 * yf / xfx) / (1.0 + yf * yf);
            
            fexc[i] += fpre * fpe1 * rho;
            
            grhob[i] += fpre * (fpe1 + rho * fpex1 * xrho);
        }
    }
    
    void
    VWN3FuncGradientB(      CXCGradientGrid& xcGradientGrid,
                      const double           factor,
                      const CDensityGrid&    densityGrid)
    {
        // paramagnetic fitting factors
        
        double pa = 0.0621814, pb = 13.0720, pc = 42.7198, px0 = -0.4092860;
        
        double pq = std::sqrt(4.0 * pc - pb * pb);
        
        double pxf0 = px0 * px0 + pb * px0 + pc;
        
        double pyf0 = pq / (pb + 2.0 * px0);
        
        double b = px0 / pxf0;
        
        double c = pxf0 * pyf0;
        
        double acon= b * pb - 1.0;
        
        double bcon = 2.0 * acon + 2.0;
        
        double ccon = 2.0 * pb * (1.0 / pq - px0 / c);
        
        // various prefactor
        
        double f16 = -1.0 / 6.0;
        
        double f76 = -7.0 / 6.0;
        
        double dcrs = std::pow(3.0 / (4.0 * mathconst::getPiValue()), -f16);
        
        double fpre = factor * 0.5 * pa;
        
        // determine number of grid points
        
        auto ngpoints = densityGrid.getNumberOfGridPoints();
        
        // set up pointers to density grid data
        
        auto rhoa = densityGrid.alphaDensity(0);
        
        // set up pointers to functional data
        
        auto fexc = xcGradientGrid.xcFunctionalValues();
        
        auto grhoa = xcGradientGrid.xcGradientValues(xcvars::rhoa);
        
        // diamagnetic contribution
        
        #pragma omp simd aligned(rhoa, fexc, grhoa: VLX_ALIGN)
        for (int32_t i = 0; i < ngpoints; i++)
        {
            double rho = rhoa[i];
            
            double x = dcrs * std::pow(rho, f16);
            
            double xrho  = dcrs * f16 * std::pow(rho, f76);
            
            double xf = x * x + pb * x + pc;
            
            double xfx = 2.0 * x + pb;
            
            double yf = pq / xfx;
            
            double fpe1 = 2.0 * std::log(x) + acon * std::log(xf) - bcon * std::log(x - px0) + ccon * std::atan(yf);
            
            double fpex1 = 2.0 / x + acon * xfx / xf - bcon / (x - px0) - ccon * (2.0 * yf / xfx) / (1.0 + yf * yf);
            
            fexc[i] += fpre * fpe1 * rho;
            
            grhoa[i] += fpre * (fpe1 + rho * fpex1 * xrho);
        }
    }
    
    void
    VWN3FuncHessianAB(      CXCHessianGrid& xcHessianGrid,
                      const double          factor,
                      const CDensityGrid&   densityGrid)
    {
        // paramagnetic fitting factors
        
        double pa = 0.0621814, pb = 13.0720, pc = 42.7198, px0 = -0.4092860;

        double pq = std::sqrt(4.0 * pc - pb * pb);
        
        double pxf0 = px0 * px0 + pb * px0 + pc;
        
        double pyf0 = pq / (pb + 2.0 * px0);
        
        double b = px0 / pxf0;
        
        double c = pxf0 * pyf0;
        
        double acon= b * pb - 1.0;
        
        double bcon = 2.0 * acon + 2.0;
        
        double ccon = 2.0 * pb * (1.0 / pq - px0 / c);
        
        // various prefactor
        
        double f16 = -1.0 / 6.0;
        
        double f76 = -7.0 / 6.0;
        
        double dcrs = std::pow(3.0 / (4.0 * mathconst::getPiValue()), -f16);
        
        double fpre = factor * 0.5 * pa;
        
        // determine number of grid points
        
        auto ngpoints = densityGrid.getNumberOfGridPoints();
        
        // set up pointers to density grid data
        
        auto rhoa = densityGrid.alphaDensity(0);
        
        auto rhob = densityGrid.betaDensity(0);
        
        // set up pointers to functional data
        
        auto grho_aa = xcHessianGrid.xcHessianValues(xcvars::rhoa, xcvars::rhoa);
        
        auto grho_ab = xcHessianGrid.xcHessianValues(xcvars::rhoa, xcvars::rhob);
        
        auto grho_bb = xcHessianGrid.xcHessianValues(xcvars::rhob, xcvars::rhob);
        
        // diamagnetic contribution
        
        #pragma omp simd aligned(rhoa, rhob, grho_aa, grho_ab, grho_bb: VLX_ALIGN)
        for (int32_t i = 0; i < ngpoints; i++)
        {
            double rho = rhoa[i] + rhob[i];
            
            double x = dcrs * std::pow(rho, f16);
            
            double xrho  = dcrs * f16 * std::pow(rho, f76);
            
            double xf = x * x + pb * x + pc;
            
            double xfx = 2.0 * x + pb;
            
            double yf = pq / xfx;
            
            double fpex1 = 2.0 / x + acon * xfx / xf - bcon / (x - px0) - ccon * (2.0 * yf / xfx) / (1.0 + yf * yf);
            
            double fpexx1 = -2.0 / (x * x) + acon * (2.0 / xf - xfx * xfx / (xf * xf))
           
                          + bcon / ((x - px0) * (x - px0)) + ccon * 8.0 * pq * xfx / ((pq * pq + xfx * xfx) * (pq * pq + xfx * xfx));
            
            double gval = fpre * xrho * (2.0 * fpex1 + rho * fpexx1 * xrho - fpex1 * 7.0 / 6.0);
            
            grho_aa[i] += gval;
            
            grho_ab[i] += gval;
            
            grho_bb[i] += gval;
        }
    }
    
    void
    VWN3FuncHessianA(      CXCHessianGrid& xcHessianGrid,
                     const double          factor,
                     const CDensityGrid&   densityGrid)
    {
        // paramagnetic fitting factors
        
        double pa = 0.0621814, pb = 13.0720, pc = 42.7198, px0 = -0.4092860;
        
        double pq = std::sqrt(4.0 * pc - pb * pb);
        
        double pxf0 = px0 * px0 + pb * px0 + pc;
        
        double pyf0 = pq / (pb + 2.0 * px0);
        
        double b = px0 / pxf0;
        
        double c = pxf0 * pyf0;
        
        double acon= b * pb - 1.0;
        
        double bcon = 2.0 * acon + 2.0;
        
        double ccon = 2.0 * pb * (1.0 / pq - px0 / c);
        
        // various prefactor
        
        double f16 = -1.0 / 6.0;
        
        double f76 = -7.0 / 6.0;
        
        double dcrs = std::pow(3.0 / (4.0 * mathconst::getPiValue()), -f16);
        
        double fpre = factor * 0.5 * pa;
        
        // determine number of grid points
        
        auto ngpoints = densityGrid.getNumberOfGridPoints();
        
        // set up pointers to density grid data
        
        auto rhob = densityGrid.betaDensity(0);
        
        // set up pointers to functional data
        
        auto grho_bb = xcHessianGrid.xcHessianValues(xcvars::rhob, xcvars::rhob);
        
        // diamagnetic contribution
        
        #pragma omp simd aligned(rhob, grho_bb: VLX_ALIGN)
        for (int32_t i = 0; i < ngpoints; i++)
        {
            double rho = rhob[i];
            
            double x = dcrs * std::pow(rho, f16);
            
            double xrho  = dcrs * f16 * std::pow(rho, f76);
            
            double xf = x * x + pb * x + pc;
            
            double xfx = 2.0 * x + pb;
            
            double yf = pq / xfx;
            
            double fpex1 = 2.0 / x + acon * xfx / xf - bcon / (x - px0) - ccon * (2.0 * yf / xfx) / (1.0 + yf * yf);
            
            double fpexx1 = -2.0 / (x * x) + acon * (2.0 / xf - xfx * xfx / (xf * xf))
           
                          + bcon / ((x - px0) * (x - px0)) + ccon * 8.0 * pq * xfx / ((pq * pq + xfx * xfx) * (pq * pq + xfx * xfx));
            
            double gval = fpre * xrho * (2.0 * fpex1 + rho * fpexx1 * xrho - fpex1 * 7.0 / 6.0);
            
            grho_bb[i] += gval;
        }
    }
    
    void
    VWN3FuncHessianB(      CXCHessianGrid& xcHessianGrid,
                      const double          factor,
                      const CDensityGrid&   densityGrid)
    {
        // paramagnetic fitting factors
        
        double pa = 0.0621814, pb = 13.0720, pc = 42.7198, px0 = -0.4092860;
        
        double pq = std::sqrt(4.0 * pc - pb * pb);
        
        double pxf0 = px0 * px0 + pb * px0 + pc;
        
        double pyf0 = pq / (pb + 2.0 * px0);
        
        double b = px0 / pxf0;
        
        double c = pxf0 * pyf0;
        
        double acon= b * pb - 1.0;
        
        double bcon = 2.0 * acon + 2.0;
        
        double ccon = 2.0 * pb * (1.0 / pq - px0 / c);
        
        // various prefactor
        
        double f16 = -1.0 / 6.0;
        
        double f76 = -7.0 / 6.0;
        
        double dcrs = std::pow(3.0 / (4.0 * mathconst::getPiValue()), -f16);
        
        double fpre = factor * 0.5 * pa;
        
        // determine number of grid points
        
        auto ngpoints = densityGrid.getNumberOfGridPoints();
        
        // set up pointers to density grid data
        
        auto rhoa = densityGrid.alphaDensity(0);
        
        // set up pointers to functional data
        
        auto grho_aa = xcHessianGrid.xcHessianValues(xcvars::rhoa, xcvars::rhoa);
        
        // diamagnetic contribution
        
        #pragma omp simd aligned(rhoa, grho_aa: VLX_ALIGN)
        for (int32_t i = 0; i < ngpoints; i++)
        {
            double rho = rhoa[i];
            
            double x = dcrs * std::pow(rho, f16);
            
            double xrho  = dcrs * f16 * std::pow(rho, f76);
            
            double xf = x * x + pb * x + pc;
            
            double xfx = 2.0 * x + pb;
            
            double yf = pq / xfx;
            
            double fpex1 = 2.0 / x + acon * xfx / xf - bcon / (x - px0) - ccon * (2.0 * yf / xfx) / (1.0 + yf * yf);
            
            double fpexx1 = -2.0 / (x * x) + acon * (2.0 / xf - xfx * xfx / (xf * xf))
           
                          + bcon / ((x - px0) * (x - px0)) + ccon * 8.0 * pq * xfx / ((pq * pq + xfx * xfx) * (pq * pq + xfx * xfx));
            
            double gval = fpre * xrho * (2.0 * fpex1 + rho * fpexx1 * xrho - fpex1 * 7.0 / 6.0);
            
            grho_aa[i] += gval;
        }
    }
    
}  // namespace vxcfuncs

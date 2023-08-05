//
//                           VELOXCHEM 1.0-RC
//      ---------------------------------------------------
//                     An Electronic Structure Code
//
//  Copyright © 2018-2020 by VeloxChem developers. All rights reserved.
//  Contact: https://veloxchem.org/contact

#include "XCFunctional.hpp"

#include <cmath>

CXCFunctional::CXCFunctional()

    : _label(std::string())

    , _xcFuncType(xcfun::undefined)

    , _fractionOfExactExchange(0.0)

    , _primitiveFunctionals(std::vector<CPrimitiveFunctional>())

    , _weightsOfPrimitiveFunctionals(std::vector<double>())
{
    
}

CXCFunctional::CXCFunctional(const std::string&                       label,
                             const xcfun                              xcFuncType,
                             const double                             fractionOfExactExchange,
                             const std::vector<CPrimitiveFunctional>& primitiveFunctionals,
                             const std::vector<double>&               weightsOfPrimitiveFunctionals)

    : _label(label)

    , _xcFuncType(xcFuncType)

    , _fractionOfExactExchange(fractionOfExactExchange)

    , _primitiveFunctionals(primitiveFunctionals)

    , _weightsOfPrimitiveFunctionals(weightsOfPrimitiveFunctionals)
{
    
}

CXCFunctional::CXCFunctional(const CXCFunctional& source)

    : _label(source._label)

    , _xcFuncType(source._xcFuncType)

    , _fractionOfExactExchange(source._fractionOfExactExchange)

    , _primitiveFunctionals(source._primitiveFunctionals)

    , _weightsOfPrimitiveFunctionals(source._weightsOfPrimitiveFunctionals)
{
    
}

CXCFunctional::CXCFunctional(CXCFunctional&& source) noexcept

    : _label(std::move(source._label))

    , _xcFuncType(std::move(source._xcFuncType))

    , _fractionOfExactExchange(std::move(source._fractionOfExactExchange))

    , _primitiveFunctionals(std::move(source._primitiveFunctionals))

    , _weightsOfPrimitiveFunctionals(std::move(source._weightsOfPrimitiveFunctionals))
{
    
}

CXCFunctional::~CXCFunctional()
{
}

CXCFunctional&
CXCFunctional::operator=(const CXCFunctional& source)
{
    if (this == &source) return *this;

    _label = source._label;

    _xcFuncType = source._xcFuncType;
    
    _fractionOfExactExchange = source._fractionOfExactExchange;
    
    _primitiveFunctionals = source._primitiveFunctionals;
    
    _weightsOfPrimitiveFunctionals = source._weightsOfPrimitiveFunctionals;

    return *this;
}

CXCFunctional&
CXCFunctional::operator=(CXCFunctional&& source) noexcept
{
    if (this == &source) return *this;

    _label = std::move(source._label);

    _xcFuncType = std::move(source._xcFuncType);
    
    _fractionOfExactExchange = std::move(source._fractionOfExactExchange);
    
    _primitiveFunctionals = std::move(source._primitiveFunctionals);
    
    _weightsOfPrimitiveFunctionals = std::move(source._weightsOfPrimitiveFunctionals);

    return *this;
}

bool
CXCFunctional::operator==(const CXCFunctional& other) const
{
    if (this == &other) return true;

    if (_label != other._label) return false;
    
    if (_xcFuncType != other._xcFuncType) return false;
    
    if (std::fabs(_fractionOfExactExchange - other._fractionOfExactExchange) > 1.0e-13) return false;
    
    if (_primitiveFunctionals.size() != other._primitiveFunctionals.size()) return false;
    
    for (size_t i = 0; i < _primitiveFunctionals.size(); i++)
    {
        if (_primitiveFunctionals[i] != other._primitiveFunctionals[i]) return false;
    }
    
    if (_weightsOfPrimitiveFunctionals.size() != other._weightsOfPrimitiveFunctionals.size()) return false;
    
    for (size_t i = 0; i < _weightsOfPrimitiveFunctionals.size(); i++)
    {
        if (std::fabs(_weightsOfPrimitiveFunctionals[i] - other._weightsOfPrimitiveFunctionals[i]) > 1.0e-13) return false;
    }

    return true;
}

bool
CXCFunctional::operator!=(const CXCFunctional& other) const
{
    return !((*this) == other);
}

void
CXCFunctional::compute(      CXCGradientGrid& xcGradientGrid,
                       const CDensityGrid&    densityGrid) const
{
    xcGradientGrid.zero();
    
    for (size_t i = 0; i < _primitiveFunctionals.size(); i++)
    {
        _primitiveFunctionals[i].compute(xcGradientGrid, _weightsOfPrimitiveFunctionals[i], densityGrid);
    }
}

void
CXCFunctional::compute(      CXCHessianGrid& xcHessianGrid,
                       const CDensityGrid&   densityGrid) const
{
    xcHessianGrid.zero();
    
    for (size_t i = 0; i < _primitiveFunctionals.size(); i++)
    {
        _primitiveFunctionals[i].compute(xcHessianGrid, _weightsOfPrimitiveFunctionals[i], densityGrid);
    }
}

std::string
CXCFunctional::getLabel() const
{
    return _label;
}

xcfun
CXCFunctional::getFunctionalType() const
{
    return _xcFuncType;
}

double
CXCFunctional::getFractionOfExactExchange() const
{
    return _fractionOfExactExchange;
}

bool
CXCFunctional::isHybridFunctional() const
{
    if (std::fabs(_fractionOfExactExchange) < 1.0e-13) return false;
    
    return true;
}

bool
CXCFunctional::isUndefined() const
{
    if (_xcFuncType == xcfun::undefined) return true;
    
    return false;
}

std::ostream&
operator<<(std::ostream& output, const CXCFunctional& source)
{
    output << std::endl;

    output << "[CXCFunctional (Object):" << &source << "]" << std::endl;

    output << "_label: " << source._label << std::endl;
    
    output << "_xcFuncType:" << to_string(source._xcFuncType);
    
    output << "_fractionOfExactExchange:" << source._fractionOfExactExchange;
    
    output << "_primitiveFunctionals: " << std::endl;
    
    for (size_t i = 0; i < source._primitiveFunctionals.size(); i++)
    {
        output << "_primitiveFunctionals[" << i << "]: " << std::endl;
        
        output << source._primitiveFunctionals[i] << std::endl;
    }
    
    output << "_weightsOfPrimitiveFunctionals: " << std::endl;
    
    for (size_t i = 0; i < source._weightsOfPrimitiveFunctionals.size(); i++)
    {
        output << "_weightsOfPrimitiveFunctionals[" << i << "]: " << std::endl;
        
        output << source._weightsOfPrimitiveFunctionals[i] << std::endl;
    }

    return output;
}

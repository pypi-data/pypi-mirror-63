//
//                           VELOXCHEM 1.0-RC
//      ---------------------------------------------------
//                     An Electronic Structure Code
//
//  Copyright © 2018-2020 by VeloxChem developers. All rights reserved.
//  Contact: https://veloxchem.org/contact

#ifndef RecursionTerm_hpp
#define RecursionTerm_hpp

#include <cstdlib>
#include <string>

#include "FourIndexes.hpp"
#include "RecursionBlock.hpp"

/**
 Class CRecursionTerm stores meta data for primitive or auxilary integral
 and provides set of methods for manipulating with meta data.

 @author Z. Rinkevicius
 */
class CRecursionTerm
{
    /**
     The label of integrand operator.
     */
    std::string _labelOfOperator;

    /**
     The tensorial order of integrand operator.
     */
    int32_t _orderOfOperator;

    /**
     The flag indicating form, full or reduced, of integrand operator.
     */
    int32_t _isReducedOperator;

    /**
     The angular momentum of bra side.
     */
    CFourIndexes _braAngularMomentum;

    /**
     The angular momentum of ket side.
     */
    CFourIndexes _ketAngularMomentum;

    /**
     The number of centers on bra side.
     */
    int32_t _braCenters;

    /**
     The number of centers on ket side.
     */
    int32_t _ketCenters;

    /**
     The order of integral.
     */
    int32_t _orderOfIntegral;

    /**
     Cheks if angular momentum is valid for given number of centers.

     @param angularMomentum the angular momentum.
     @param nCenters the number of centers.
     @return true if angular momentum is valids, false otherwise.
     */
    bool _isValidAngularMomentum(const CFourIndexes& angularMomentum, const int32_t nCenters) const;

    /**
     Getts number of Cartesian components for angular momentum with specified
     number of centers.

     @param angularMomentum the angular momentum.
     @param nCenters the number of centers.
     @return the number of Cartesian components.
     */
    int32_t _numberOfCartesianComponents(const CFourIndexes& angularMomentum, const int32_t nCenters) const;

    /**
     Getts number of spherical components for angular momentum with specified
     number of centers.

     @param angularMomentum the angular momentum.
     @param nCenters the number of centers.
     @return the number of spherical components.
     */
    int32_t _numberOfSphericalComponents(const CFourIndexes& angularMomentum, const int32_t nCenters) const;

   public:
    /**
     Creates an empty recursion term object.
     */
    CRecursionTerm();

    /**
     Creates a recursion term object from given meta data.

     @param labelOfOperator the label of integrand operator.
     @param orderOfOperator the tensorial order of integrand operator.
     @param isReducedOperator the form of integrand operator: reduced or full
            tensor.
     @param braAngularMomentum the angular momentum of bra side.
     @param ketAngularMomentum the angular momentum of ket side.
     @param braCenters the number of GTO centers on bra side.
     @param ketCenters the number of GTO centers on ket side.
     @param orderOfIntegral the order of integral.
     */
    CRecursionTerm(const std::string&  labelOfOperator,
                   const int32_t       orderOfOperator,
                   const bool          isReducedOperator,
                   const CFourIndexes& braAngularMomentum,
                   const CFourIndexes& ketAngularMomentum,
                   const int32_t       braCenters,
                   const int32_t       ketCenters,
                   const int32_t       orderOfIntegral);

    /**
     Creates a recursion term object by copying other recursion term object.

     @param source the recursion term object.
     */
    CRecursionTerm(const CRecursionTerm& source);

    /**
     Creates a recursion term object by moving other recursion term object.

     @param source the recursion term object.
     */
    CRecursionTerm(CRecursionTerm&& source) noexcept;

    /**
     Destroys a recursion term object.
     */
    ~CRecursionTerm();

    /**
     Assigns a recursion term object by copying other recursion term object.

     @param source the recursion term object.
     */
    CRecursionTerm& operator=(const CRecursionTerm& source);

    /**
     Assigns a recursion term object by moving other recursion term object.

     @param source the recursion term object.
     */
    CRecursionTerm& operator=(CRecursionTerm&& source) noexcept;

    /**
     Compares recursion term object with other recursion term object.

     @param other the recursion term object.
     @return true if recursion term objects are equal, false otherwise.
     */
    bool operator==(const CRecursionTerm& other) const;

    /**
     Compares recursion term object with other recursion term object.

     @param other the recursion term object.
     @return true if recursion term objects are not equal, false otherwise.
     */
    bool operator!=(const CRecursionTerm& other) const;

    /**
     Sets label of operator in recursion term object.

     @param labelOfOperator the label of operator.
     */
    void setLabel(const std::string labelOfOperator);

    /**
     Sets order of integrals in recursion term object.

     @param orderOfIntegral the order of integral.
     */
    void setOrder(const int32_t orderOfIntegral);

    /**
     Creates recursion term object with shifted angular momentum on bra side.

     @param braValue the shift value of angular momentum component.
     @param braCenter the identifier of angular center on bra side.
     @return the recursion term object.
     */
    CRecursionTerm braShift(const int32_t braValue, const int32_t braCenter) const;

    /**
     Creates recursion term object with shifted angular momentum on ket side.

     @param ketValue the shift value of angular momentum component.
     @param ketCenter the identifier of angular center on ket side.
     @return the recursion term object.
     */
    CRecursionTerm ketShift(const int32_t ketValue, const int32_t ketCenter) const;

    /**
     Creates recursion term object with shifted order of integral.

     @param orderValue the shift value for order of integral.
     @return the recursion term object.
     */
    CRecursionTerm orderShift(const int32_t orderValue) const;

    /**
     Creates recursion term object with shifted order of integrand operator.

     @param operatorValue the shift value for order of integrand operator.
     @return the recursion term object.
     */
    CRecursionTerm operatorShift(const int32_t operatorValue) const;

    /**
     Checks if recursion term object is valid recursion term.

     @return true if recursion term object is valid recursion term, false otherwise.
     */
    bool isValid() const;

    /**
     Checks if angular momentum on bra side is of zero order i.e. (0, 0, 0,...).

     @return true if angular momentum on bra side is of zero order,
             false otherwise.
     */
    bool isBraOfZeroOrder() const;

    /**
     Gets label of integrand in recursion term object.

     @return the label of integrand.
     */
    std::string getLabel() const;

    /**
     Gets order of integral in recursion term object.

     @return the order of integral.
     */
    int32_t getOrder() const;

    /**
     Gets number of tensorial components of integrand operator.

     @return the number of tensorial components.
     */
    int32_t getNumberOfOperatorComponents() const;

    /**
     Gets number of Cartesian components on bra side.

     @return the number of Cartesian components.
     */
    int32_t braCartesianComponents() const;

    /**
     Gets number of Cartesian components on ket side.

     @return the number of Cartesian components.
     */
    int32_t ketCartesianComponents() const;

    /**
     Gets number of spherical components on bra side.

     @return the number of Cartesian components.
     */
    int32_t braSphericalComponents() const;

    /**
     Gets number of spherical components on ket side.

     @return the number of Cartesian components.
     */
    int32_t ketSphericalComponents() const;

    /**
     Gets number of components in integral.

     @param angularForm the angular form of integral.
     @return the number of components.
     */
    int32_t getNumberOfComponents(const recblock angularForm) const;
    
    /**
     Gets angular momentum of specific center on bra side of integral.

     @param iCenter the index of atomic center.
     @return the angular momentum of atomic center.
     */
    int32_t getBraAngularMomentum(const int32_t iCenter) const;
    
    /**
     Gets angular momentum of specific center on ket side of integral.
     
     @param iCenter the index of atomic center.
     @return the angular momentum of atomic center.
     */
    int32_t getKetAngularMomentum(const int32_t iCenter) const;

    /**
     Checks if recursion term object is integral with specific label, bra and
     ket sides.

     @param label the label of operator.
     @param braAngularMomentum the angular momentum of bra side.
     @param ketAngularMomentum the angular momentum of ket side.
     @param braCenters the number of centers on bra side.
     @param ketCenters the number of centers on ket side.
     @return true if recurion object is specified integral, false - otherwise.
     */
    bool isIntegral(const std::string&  label,
                    const CFourIndexes& braAngularMomentum,
                    const CFourIndexes& ketAngularMomentum,
                    const int32_t       braCenters,
                    const int32_t       ketCenters) const;

    /**
     Converts recursion term object to text output and insert it into output
     text stream.

     @param output the output text stream.
     @param source the recursion term object.
     */
    friend std::ostream& operator<<(std::ostream& output, const CRecursionTerm& source);
};

#endif /* RecursionTerm_hpp */

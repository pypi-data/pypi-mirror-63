//
//                           VELOXCHEM 1.0-RC
//      ---------------------------------------------------
//                     An Electronic Structure Code
//
//  Copyright © 2018-2020 by VeloxChem developers. All rights reserved.
//  Contact: https://veloxchem.org/contact

#ifndef DenseDiagonalizer_hpp
#define DenseDiagonalizer_hpp

#include "DenseMatrix.hpp"
#include "MemBlock.hpp"

/**
 Class CDenseDiagonalizer provides methods for diagonalization of dense real
 symmetric matrices and for manipulation with computed eigenvalues and
 eigenvectors.

 @author Z. Rinkevicius
 */
class CDenseDiagonalizer
{
    /**
     The state of dense diagonalizer object : true - no errors,
     false - otherwise.
     */
    bool _state;

    /**
     The availability of eigenvalues and eigenvectors: true - available,
     false - otherwise.
     */
    bool _isSolved;

    /**
     The temporary dense matrix used by diagonalization routine.
     */
    CDenseMatrix _matrix;

    /**
     The eigenvectors of dense matrix.
     */
    CDenseMatrix _eigenVectors;

    /**
     The eigenvalues of dense matrix.
     */
    CMemBlock<double> _eigenValues;

   public:
    /**
     Creates an dense diagonalizer object.
     */
    CDenseDiagonalizer();

    /**
     Destroys a dense diagonalizer object.
     */
    ~CDenseDiagonalizer();

    /**
     Diagonalizes dense matrix and stores eigenvalues/eigenvectors into internal
     data buffers.

     @param matrix the dense matrix.
     */
    void diagonalize(const CDenseMatrix& matrix);

    /**
     Gets state of dense diagonalizer object.

     @return true if no errors, false otherwise.
     */
    bool getState() const;

    /**
     Check if basis of solution vectors is linearly dependent.

     @param threshold the linear dependence threshold.
     @return true if basis is linearly dependent, false otherwise.
     */
    bool isLinearlyDependentBasis(const double threshold) const;

    /**
     Gets eigenvectors of dense matrix.

     @return the eigenvectors of matrix.
     */
    CDenseMatrix getEigenVectors() const;

    /**
     Gets eigenvectors of dense matrix above specifc threshold.

     @param threshold the cut-off threshold for eigenvalues.
     @return the eigenvectors of matrix.
     */
    CDenseMatrix getEigenVectors(const double threshold) const;

    /**
     Gets eigenvalues of dense matrix.

     @return the eigenvalues of matrix.
     */
    CMemBlock<double> getEigenValues() const;

    /**
     Gets eigenvalues of dense matrix above specifc threshold.

     @param threshold the cut-off threshold for eigenvalues.
     @return the eigenvalues of matrix.
     */
    CMemBlock<double> getEigenValues(const double threshold) const;

    /**
     Computes A^-1/2 matrix using eigenvalues and eigenvectors of A matrix.

     @return the A^-1/2 matrix.
     */
    CDenseMatrix getInvertedSqrtMatrix() const;

    /**
     Computes A^-1 matrix using eigenvalues and eigenvectors of A matrix.

     @return the A^-1 matrix.
     */
    CDenseMatrix getInvertedMatrix() const;

    /**
     Gets number of eigenvalues bellow given threshold.

     @param threshold the eigenvalues cut-off threshold.
     @return the number of eigenvalues.
     */
    int32_t getNumberOfEigenValues(const double threshold) const;
};

#endif /* DenseDiagonalizer_hpp */

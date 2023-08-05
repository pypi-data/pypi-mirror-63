//
//                           VELOXCHEM 1.0-RC
//      ---------------------------------------------------
//                     An Electronic Structure Code
//
//  Copyright © 2018-2020 by VeloxChem developers. All rights reserved.
//  Contact: https://veloxchem.org/contact

#include "GenFunc.hpp"

#include "AngularMomentum.hpp"

namespace genfunc {  // genfunc namespace

void
contract(      CMemBlock2D<double>& contrData,
         const CMemBlock2D<double>& primData,
         const int32_t              contrIndex,
         const int32_t              primIndex,
         const int32_t*             startPositions,
         const int32_t*             endPositions,
         const int32_t              nElements,
         const int32_t              nBlocks)
{
    for (int32_t i = 0; i < nBlocks; i++)
    {
        // set up data vectors

        auto pdat = primData.data(primIndex + i);

        auto cdat = contrData.data(contrIndex + i);

        for (int32_t j = 0; j < nElements; j++)
        {
            double fsum = 0.0;

            // contract data vector components

            for (int32_t k = startPositions[j]; k < endPositions[j]; k++)
            {
                fsum += pdat[k];
            }

            cdat[j] = fsum;
        }
    }
}

void
contract(CMemBlock2D<double>& contrData,
         CMemBlock2D<double>& primData,
         const int32_t        primIndex,
         const CGtoBlock&     braGtoBlock,
         const CGtoBlock&     ketGtoBlock,
         const int32_t        iContrGto)
{
    // set up angular momentum

    auto bang = braGtoBlock.getAngularMomentum();

    auto kang = ketGtoBlock.getAngularMomentum();

    auto ncomp = angmom::to_CartesianComponents(bang, kang);

    // set up pointers to primitives data on bra side

    auto spos = braGtoBlock.getStartPositions();

    auto epos = braGtoBlock.getEndPositions();

    auto bdim = epos[iContrGto] - spos[iContrGto];

    // set up pointers to primitives data on ket side

    auto nprim = ketGtoBlock.getNumberOfPrimGtos();

    // first step: vertical summation over bra GTO

    for (int32_t i = 1; i < bdim; i++)
    {
        // accumulate summation over primitives on bra side

        for (int32_t j = 0; j < ncomp; j++)
        {
            // summation buffer

            auto sumbuf = primData.data(primIndex + j);

            // source buffer

            auto srcbuf = primData.data(primIndex + i * ncomp + j);

            // loop over primitive GTOs on ket side

            #pragma omp simd aligned(sumbuf, srcbuf: VLX_ALIGN)
            for (int32_t k = 0; k < nprim; k++)
            {
                sumbuf[k] += srcbuf[k];
            }
        }
    }

    // reset primitive GTOs indexing pointers to ket side

    spos = ketGtoBlock.getStartPositions();

    epos = ketGtoBlock.getEndPositions();

    auto kdim = ketGtoBlock.getNumberOfContrGtos();

    // second step: direct contraction over ket side

    genfunc::contract(contrData, primData, 0, primIndex, spos, epos, kdim, ncomp);
}

void
contract(      CMemBlock2D<double>& contrData,
               CMemBlock2D<double>* primData,
         const CRecursionMap&       contractionMap,
         const CRecursionMap&       recursionMap,
         const CGtoPairsBlock&      braGtoPairsBlock,
         const CGtoPairsBlock&      ketGtoPairsBlock,
         const int32_t              nKetPrimPairs,
         const int32_t              nKetContrPairs,
         const int32_t              iContrPair)
{
    // set up pointers to primitives data on bra side

    auto spos = braGtoPairsBlock.getStartPositions();

    auto epos = braGtoPairsBlock.getEndPositions();

    auto bdim = epos[iContrPair] - spos[iContrPair];

    // set up pointers to primitives data on ket side

    auto kspos = ketGtoPairsBlock.getStartPositions();

    auto kepos = ketGtoPairsBlock.getEndPositions();

    // loop over set of data vectors

    for (int32_t i = 0; i < contractionMap.getNumberOfTerms(); i++)
    {
        auto rterm = contractionMap.getTerm(i);
        
        if (rterm.getKetAngularMomentum(0) == 0)
        {
            // determine positions of contracted and primitive vectors

            auto cidx = contractionMap.getIndexOfTerm(rterm);

            auto pidx = recursionMap.index(CRecursionTerm({"Electron Repulsion"}, 0, true,
                                                          {rterm.getBraAngularMomentum(0), -1, -1, -1},
                                                          {rterm.getKetAngularMomentum(1), -1, -1, -1},
                                                          1, 1, 0));

            // set up number angular components

            auto ncomp = angmom::to_CartesianComponents(rterm.getBraAngularMomentum(0), rterm.getKetAngularMomentum(1));

            // first step: vertical summation over bra GTO

            for (int32_t j = 1; j < bdim; j++)
            {
                // accumulate summation over primitives on bra side

                for (int32_t k = 0; k < ncomp; k++)
                {
                    // summation buffer

                    auto sumbuf = primData[pidx].data(k);

                    // source buffer

                    auto srcbuf = primData[pidx].data(j * ncomp + k);

                    // loop over primitive GTOs on ket side

                    #pragma omp simd aligned(sumbuf, srcbuf: VLX_ALIGN)
                    for (int32_t l = 0; l < nKetPrimPairs; l++)
                    {
                        sumbuf[l] += srcbuf[l];
                    }
                }
            }
            
            // second step: direct contraction over ket side

            genfunc::contract(contrData, primData[pidx], cidx, 0, kspos, kepos, nKetContrPairs, ncomp);
        }
    }
}

void
transform(CMemBlock2D<double>&       spherData,
          const CMemBlock2D<double>& cartData,
          const CSphericalMomentum&  spherMomentum,
          const int32_t              spherIndex,
          const int32_t              cartIndex,
          const int32_t              nElements,
          const int32_t              nBlocks)
{
    auto ncomp = spherMomentum.getNumberOfComponents();

    for (int32_t i = 0; i < ncomp; i++)
    {
        // set up Cartesian to spherical transformation data

        auto nfact = spherMomentum.getNumberOfFactors(i);

        auto tidx = spherMomentum.getIndexes(i);

        auto tfact = spherMomentum.getFactors(i);

        for (int32_t j = 0; j < nBlocks; j++)
        {
            // set up spherical data vector

            auto sphervec = spherData.data(spherIndex + i * nBlocks + j);

            // first term: assignment

            auto cartvec = cartData.data(cartIndex + tidx[0] * nBlocks + j);

            auto cfact = tfact[0];

            #pragma omp simd aligned(sphervec, cartvec: VLX_ALIGN)
            for (int32_t k = 0; k < nElements; k++)
            {
                sphervec[k] = cfact * cartvec[k];
            }

            // remaining terms: addition

            for (int32_t k = 1; k < nfact; k++)
            {
                cartvec = cartData.data(tidx[k] * nBlocks + j);

                cfact = tfact[k];

                #pragma omp simd aligned(sphervec, cartvec: VLX_ALIGN)
                for (int32_t l = 0; l < nElements; l++)
                {
                    sphervec[l] += cfact * cartvec[l];
                }
            }
        }
    }
}

void
transform(      CMemBlock2D<double>& spherData,
          const CMemBlock2D<double>& cartData,
          const CSphericalMomentum&  braMomentum,
          const CSphericalMomentum&  ketMomentum,
          const int32_t              spherIndex,
          const int32_t              cartIndex,
          const int32_t              nElements)
{
    // set up angular momentum data

    auto bcomp = braMomentum.getNumberOfComponents();

    auto kcomp = ketMomentum.getNumberOfComponents();

    // set up number of Cartisian components on ket side

    auto kcart = angmom::to_CartesianComponents(ketMomentum.getAngularMomentum());

    // loop over spherical components on bra side

    for (int32_t i = 0; i < bcomp; i++)
    {
        // set up transformation data for bra side

        auto bnfact = braMomentum.getNumberOfFactors(i);

        auto btidx = braMomentum.getIndexes(i);

        auto btfact = braMomentum.getFactors(i);

        // loop over spherical components on ket side

        for (int32_t j = 0; j < kcomp; j++)
        {
            // set up transformation data for ket side

            auto knfact = ketMomentum.getNumberOfFactors(j);

            auto ktidx = ketMomentum.getIndexes(j);

            auto ktfact = ketMomentum.getFactors(j);

            // set up spherical integrals vector

            auto sphervec = spherData.data(spherIndex + i * kcomp + j);

            // zero spherical integrals vector

            mathfunc::zero(sphervec, nElements);

            // apply Cartesian to spherical transformation

            for (int32_t k = 0; k < bnfact; k++)
            {
                for (int32_t l = 0; l < knfact; l++)
                {
                    // set up pointer to Cartesian component

                    auto cartvec = cartData.data(cartIndex + btidx[k] * kcart + ktidx[l]);

                    auto cfact = btfact[k] * ktfact[l];

                    // loop over integrals

                    #pragma omp simd aligned(sphervec, cartvec: VLX_ALIGN)
                    for (int32_t m = 0; m < nElements; m++)
                    {
                        sphervec[m] += cfact * cartvec[m];
                    }
                }
            }
        }
    }
}

void
transform(CMemBlock2D<double>&        spherData,
          const CMemBlock2D<double>&  cartData,
          const CSphericalMomentum&   spherMomentum,
          const CVecThreeIndexes&     spherPattern,
          const std::vector<int32_t>& spherIndexes,
          const CVecThreeIndexes&     cartPattern,
          const std::vector<int32_t>& cartIndexes,
          const int32_t               nElements)
{
    for (size_t i = 0; i < cartPattern.size(); i++)
    {
        // determine positions of Cartesian and spherical data vectors

        auto tidx = cartPattern[i];

        auto cidx = genfunc::findTripleIndex(cartIndexes, cartPattern, tidx);

        auto sidx = genfunc::findTripleIndex(spherIndexes, spherPattern, {tidx.first(), 0, tidx.second()});

        // transform data vectors

        genfunc::transform(spherData, cartData, spherMomentum, sidx, cidx, nElements, angmom::to_CartesianComponents(tidx.second()));
    }
}

void
transform(CMemBlock2D<double>&       spherData,
          const CMemBlock2D<double>& cartData,
          const CSphericalMomentum&  ketMomentumC,
          const CSphericalMomentum&  ketMomentumD,
          const int32_t              spherIndex,
          const int32_t              cartIndex,
          const int32_t              nElements,
          const int32_t              nBlocks)
{
    // set up angular momentum for ket side

    auto cang = ketMomentumC.getAngularMomentum();

    auto dang = ketMomentumD.getAngularMomentum();

    // set up number of components

    auto ncart = angmom::to_CartesianComponents(cang, dang);

    auto nspher = angmom::to_SphericalComponents(cang, dang);

    // loop over components on bra side

    for (int32_t i = 0; i < nBlocks; i++)
    {
        auto sidx = spherIndex + i * nspher;

        auto cidx = cartIndex + i * ncart;

        genfunc::transform(spherData, cartData, ketMomentumC, ketMomentumD, sidx, cidx, nElements);
    }
}

void
transform_ket(CMemBlock2D<double>&        spherData,
              const CMemBlock2D<double>&  cartData,
              const CSphericalMomentum&   ketMomentumC,
              const CSphericalMomentum&   ketMomentumD,
              const CRecursionMap&        spherPattern,
              const CRecursionMap&        cartPattern,
              const CGtoPairsBlock&       ketGtoPairsBlock,
              const int32_t               nKetContrPairs,
              const int32_t               iContrPair)
{
    // loop over set of data vectors

    for (int32_t i = 0; i < spherPattern.getNumberOfTerms(); i++)
    {
        auto rterm = spherPattern.getTerm(i);
        
        // skip terms not presented in Cartesian integrals buffer

        if (rterm.getBraAngularMomentum(0) != 0) continue;
 
        // set up spherical and Cartesian data indexes

        auto sidx = spherPattern.getIndexOfTerm(rterm);

        auto cidx = cartPattern.getIndexOfTerm(CRecursionTerm({"Electron Repulsion"}, 0, true,
                                                              {rterm.getBraAngularMomentum(1), -1, -1, -1},
                                                              {rterm.getKetAngularMomentum(0), rterm.getKetAngularMomentum(1), -1, -1},
                                                              1, 2, 0));
        // set up number of bra components

        auto bcomp = angmom::to_CartesianComponents(rterm.getBraAngularMomentum(1));

        // transform ket side of integrals from Cartesian to spherical form

        transform(spherData, cartData, ketMomentumC, ketMomentumD, sidx, cidx, nKetContrPairs, bcomp);
    }
}

void
transform_bra(CMemBlock2D<double>&        spherData,
              const CMemBlock2D<double>&  cartData,
              const CSphericalMomentum&   braMomentumA,
              const CSphericalMomentum&   braMomentumB,
              const CRecursionMap&        cartPattern,
              const CGtoPairsBlock&       ketGtoPairsBlock,
              const int32_t               nKetContrPairs,
              const int32_t               iContrPair)
{
    // set up angular momentum on ket side

    auto cang = ketGtoPairsBlock.getBraAngularMomentum();

    auto dang = ketGtoPairsBlock.getKetAngularMomentum();

    // set up angulat momentum on bra side

    auto aang = braMomentumA.getAngularMomentum();

    auto bang = braMomentumB.getAngularMomentum();

    // determine Cartesian index

    auto cidx = cartPattern.getIndexOfTerm(CRecursionTerm({"Electron Repulsion"}, 0, true,
                                                {aang, bang, -1, -1},
                                                {cang, dang, -1, -1},
                                                2, 2, 0));

    // set up angular momentum data

    auto acomp = braMomentumA.getNumberOfComponents();

    auto bcomp = braMomentumB.getNumberOfComponents();

    // set up number of Cartisian components on B center

    auto bcart = angmom::to_CartesianComponents(bang);

    // set up number of spherical components on ket side

    auto kcomp = angmom::to_SphericalComponents(cang, dang);

    // loop over spherical components on bra side

    for (int32_t i = 0; i < acomp; i++)
    {
        // set up transformation data for A center

        auto anfact = braMomentumA.getNumberOfFactors(i);

        auto atidx = braMomentumA.getIndexes(i);

        auto atfact = braMomentumA.getFactors(i);

        for (int32_t j = 0; j < bcomp; j++)
        {
            // set up transformation data for B center

            auto bnfact = braMomentumB.getNumberOfFactors(j);

            auto btidx = braMomentumB.getIndexes(j);

            auto btfact = braMomentumB.getFactors(j);

            // loop over ket side spherical components

            for (int32_t k = 0; k < kcomp; k++)
            {
                // set up spherical integrals vector

                auto sphervec = spherData.data((i * bcomp + j) * kcomp + k);

                // zero spherical integrals vector

                mathfunc::zero(sphervec, nKetContrPairs);

                // apply Cartesian to spherical transformation

                for (int32_t l = 0; l < anfact; l++)
                {
                    for (int32_t m = 0; m < bnfact; m++)
                    {
                        // set up pointer to Cartesian component

                        auto cartvec = cartData.data(cidx + (atidx[l] * bcart + btidx[m]) * kcomp + k);

                        auto cfact = atfact[l] * btfact[m];

                        // loop over integrals

                        #pragma omp simd aligned(sphervec, cartvec: VLX_ALIGN)
                        for (int32_t n = 0; n < nKetContrPairs; n++)
                        {
                            sphervec[n] += cfact * cartvec[n];
                        }
                    }
                }
            }
        }
    }
}

void
compress(CSparseMatrix&             sparseMatrix,
         CMemBlock<double>&         rowValues,
         CMemBlock<int32_t>&        colIndexes,
         const CMemBlock2D<double>& spherData,
         const CGtoBlock&           braGtoBlock,
         const CGtoBlock&           ketGtoBlock,
         const int32_t              iContrGto)
{
    // set up angular momentum components

    auto bcomp = angmom::to_SphericalComponents(braGtoBlock.getAngularMomentum());

    auto kcomp = angmom::to_SphericalComponents(ketGtoBlock.getAngularMomentum());

    // set up number of contracted GTOs on ket side

    auto kdim = ketGtoBlock.getNumberOfContrGtos();

    // set up pointers to temporary row data of sparse matrix

    auto rdat = rowValues.data();

    auto cidx = colIndexes.data();

    // set up threshold

    double fthr = sparseMatrix.getThreshold();

    // loop over bra componets

    for (int32_t i = 0; i < bcomp; i++)
    {
        // reset number of elements in vector

        int32_t nelem = 0;

        // loop over ket components

        for (int32_t j = 0; j < kcomp; j++)
        {
            // set up pointer to integrals

            auto vals = spherData.data(i * kcomp + j);

            auto vids = ketGtoBlock.getIdentifiers(j);

            // loop over integrals

            for (int32_t k = 0; k < kdim; k++)
            {
                if (std::fabs(vals[k]) > fthr)
                {
                    rdat[nelem] = vals[k];

                    cidx[nelem] = vids[k];

                    nelem++;
                }
            }
        }

        // add row to sparce matrix

        if (nelem > 0)
        {
            sparseMatrix.append(rowValues, colIndexes, nelem, iContrGto * bcomp + i);
        }
    }
}

CSparseMatrix
distribute(const CSparseMatrix* listOfMatrices, const CGtoContainer* braGtoContainer, const CGtoContainer* ketGtoContainer)
{
    // set up number of atomic orbitals

    auto btao = braGtoContainer->getNumberOfAtomicOrbitals();

    auto ktao = ketGtoContainer->getNumberOfAtomicOrbitals();

    // retrieve the threshold

    auto fthr = listOfMatrices[0].getThreshold();

    // initialize sparse matrix

    CSparseMatrix spmat(btao, ktao, fthr);

    // set up temporary row data

    CMemBlock<double> rowvec(ktao);

    CMemBlock<int32_t> rowidx(ktao);

    // set up number of GTOs blocks

    auto bdim = braGtoContainer->getNumberOfGtoBlocks();

    auto kdim = ketGtoContainer->getNumberOfGtoBlocks();

    // loop over GTOs blocks on bra side

    for (int32_t i = 0; i < bdim; i++)
    {
        // set up data on bra side

        auto bcomp = angmom::to_SphericalComponents(braGtoContainer->getAngularMomentum(i));

        auto bcgto = braGtoContainer->getNumberOfContrGtos(i);

        // loop over angular componets on bra side

        for (int32_t j = 0; j < bcomp; j++)
        {
            // set up pointer to indexes of contracted GTOs on bra side

            auto bids = braGtoContainer->getIdentifiers(i, j);

            // loop over contracted GTOs on bra side

            for (int32_t k = 0; k < bcgto; k++)
            {
                // reset number of elements in sparse matrix row

                int32_t nelem = 0;

                // set up row offset for all submatrices

                auto koff = bcomp * k + j;

                // add submatrices contributions to sparse matrix row

                for (int32_t l = 0; l < kdim; l++)
                {
                    // set submatrix offset

                    auto loff = i * bdim + l;

                    // add submatrix row data to sparse matrix row data

                    auto celem = listOfMatrices[loff].getNumberOfElements(koff);

                    if (celem > 0)
                    {
                        // set up pointers to submatrix

                        auto rdat = listOfMatrices[loff].row(koff);

                        auto ridx = listOfMatrices[loff].indexes(koff);

                        // copy submatrix data

                        mathfunc::copy(rowvec.data(), nelem, rdat, 0, celem);

                        mathfunc::copy(rowidx.data(), nelem, ridx, 0, celem);

                        nelem += celem;
                    }
                }

                // add row to sparse matrix

                if (nelem > 0)
                {
                    spmat.append(rowvec, rowidx, nelem, bids[k]);
                }
            }
        }
    }

    return spmat;
}

bool
isInVector(const CVecTwoIndexes& vector, const CTwoIndexes& pair)
{
    for (size_t i = 0; i < vector.size(); i++)
    {
        if (pair == vector[i]) return true;
    }

    return false;
}

bool
isInVector(const CVecThreeIndexes& vector, const CThreeIndexes& triple)
{
    for (size_t i = 0; i < vector.size(); i++)
    {
        if (triple == vector[i]) return true;
    }

    return false;
}

bool
isInVector(const CVecFourIndexes& vector, const CFourIndexes& quadruple)
{
    for (size_t i = 0; i < vector.size(); i++)
    {
        if (quadruple == vector[i]) return true;
    }

    return false;
}

bool
addValidAndUniquePair(CVecTwoIndexes& vector, const CTwoIndexes& pair)
{
    if (!pair.isValidPair()) return false;

    if (genfunc::isInVector(vector, pair)) return false;

    vector.push_back(pair);

    return true;
}

bool
addValidAndUniqueTriple(CVecThreeIndexes& vector, const CThreeIndexes& triple)
{
    if (!triple.isValidTriple()) return false;

    if (genfunc::isInVector(vector, triple)) return false;

    vector.push_back(triple);

    return true;
}

bool
addValidAndUniqueQuadruple(CVecFourIndexes& vector, const CFourIndexes& quadruple)
{
    if (!quadruple.isValidQuadruple()) return false;

    if (genfunc::isInVector(vector, quadruple)) return false;

    vector.push_back(quadruple);

    return true;
}

int32_t
findPairIndex(const std::vector<int32_t>& indexes, const CVecTwoIndexes& vector, const CTwoIndexes& pair)
{
    for (size_t i = 0; i < vector.size(); i++)
    {
        if (pair == vector[i]) return indexes[i];
    }

    return -1;
}

int32_t
findTripleIndex(const std::vector<int32_t>& indexes, const CVecThreeIndexes& vector, const CThreeIndexes& triple)
{
    for (size_t i = 0; i < vector.size(); i++)
    {
        if (triple == vector[i]) return indexes[i];
    }

    return -1;
}

int32_t
findQuadrupleIndex(const std::vector<int32_t>& indexes, const CVecFourIndexes& vector, const CFourIndexes& quadruple)
{
    for (size_t i = 0; i < vector.size(); i++)
    {
        if (quadruple == vector[i]) return indexes[i];
    }

    return -1;
}

int32_t
maxOrderOfPair(const CVecThreeIndexes& vector, const int32_t firstIndex, const int32_t secondIndex)
{
    int32_t iord = -1;

    for (size_t i = 0; i < vector.size(); i++)
    {
        if ((vector[i].first() == firstIndex) && (vector[i].second() == secondIndex))
        {
            if (vector[i].third() > iord) iord = vector[i].third();
        }
    }

    return iord;
}

int32_t
maxOrderOfPair(const CVecFourIndexes& vector, const int32_t firstIndex, const int32_t secondIndex)
{
    int32_t iord = -1;

    for (size_t i = 0; i < vector.size(); i++)
    {
        if ((vector[i].first() == firstIndex) && (vector[i].second() == secondIndex))
        {
            if (vector[i].third() > iord) iord = vector[i].third();
        }
    }

    return iord;
}

int32_t
maxOrderOfTriple(const CVecFourIndexes& vector, const int32_t firstIndex, const int32_t secondIndex, const int32_t thirdIndex)
{
    int32_t iord = -1;

    for (size_t i = 0; i < vector.size(); i++)
    {
        if ((vector[i].first() == firstIndex) && (vector[i].second() == secondIndex) && (vector[i].fourth() == thirdIndex))
        {
            if (vector[i].third() > iord) iord = vector[i].third();
        }
    }

    return iord;
}

CVecThreeIndexes
getPairsFromTripleIndexes(const CVecThreeIndexes& vector)
{
    CVecThreeIndexes xyvec;

    for (size_t i = 0; i < vector.size(); i++)
    {
        if (vector[i].second() == 0)
        {
            xyvec.push_back(CThreeIndexes(vector[i].first(), vector[i].third(), 0));
        }
    }

    return xyvec;
}

CVecThreeIndexes
getTriplesFromQuadrupleIndexes(const CVecFourIndexes& vector)
{
    CVecThreeIndexes xyzvec;

    for (size_t i = 0; i < vector.size(); i++)
    {
        if (vector[i].first() == 0)
        {
            xyzvec.push_back(CThreeIndexes(vector[i].second(), vector[i].third(), vector[i].fourth()));
        }
    }

    return xyzvec;
}

void
compTensorTwoFromVector(CMemBlock2D<double>& tensor, const int32_t iVectorPosition, const int32_t iTensorPosition)
{
    // set up pointers to vector x, y, z

    auto rx = tensor.data(iVectorPosition);

    auto ry = tensor.data(iVectorPosition + 1);

    auto rz = tensor.data(iVectorPosition + 2);

    // set up second order tensor components

    auto rxx = tensor.data(iTensorPosition);

    auto rxy = tensor.data(iTensorPosition + 1);

    auto rxz = tensor.data(iTensorPosition + 2);

    auto ryy = tensor.data(iTensorPosition + 3);

    auto ryz = tensor.data(iTensorPosition + 4);

    auto rzz = tensor.data(iTensorPosition + 5);

    // compute second order tensor

    auto ndim = tensor.size(iVectorPosition);

    #pragma omp simd aligned(rx, ry, rz, rxx, rxy, rxz, ryy, ryz, rzz: VLX_ALIGN)
    for (int32_t i = 0; i < ndim; i++)
    {
        // leading x component

        rxx[i] = rx[i] * rx[i];

        rxy[i] = rx[i] * ry[i];

        rxz[i] = rx[i] * rz[i];

        // leading y component

        ryy[i] = ry[i] * ry[i];

        ryz[i] = ry[i] * rz[i];

        // leading x component

        rzz[i] = rz[i] * rz[i];
    }
}

void
compTensorFromVectorAndTensor(CMemBlock2D<double>& tensor,
                              const int32_t        iVectorPosition,
                              const int32_t        iTensorOnePosition,
                              const int32_t        iTensorTwoPosition,
                              const int32_t        tensorOrder)
{
    if (tensorOrder > 2)
    {
        // set up pointers to vector x, y, z

        auto rx = tensor.data(iVectorPosition);

        auto ry = tensor.data(iVectorPosition + 1);

        auto rz = tensor.data(iVectorPosition + 2);

        // set up dimensions of lower order tensors

        auto curdim = angmom::to_CartesianComponents(tensorOrder);

        auto lowdim = angmom::to_CartesianComponents(tensorOrder - 1);

        auto reddim = angmom::to_CartesianComponents(tensorOrder - 2);

        // leading x component

        auto ndim = tensor.size(iVectorPosition);

        for (int32_t i = 0; i < lowdim; i++)
        {
            auto rdst = tensor.data(iTensorTwoPosition + i);

            auto rsrc = tensor.data(iTensorOnePosition + i);

            #pragma omp simd aligned(rx, rdst, rsrc: VLX_ALIGN)
            for (int32_t j = 0; j < ndim; j++)
            {
                rdst[j] = rx[j] * rsrc[j];
            }
        }

        // leading y component

        auto yoff = lowdim - reddim;

        for (int32_t i = reddim; i < lowdim; i++)
        {
            auto rdst = tensor.data(iTensorTwoPosition + yoff + i);

            auto rsrc = tensor.data(iTensorOnePosition + i);

            #pragma omp simd aligned(ry, rdst, rsrc: VLX_ALIGN)
            for (int32_t j = 0; j < ndim; j++)
            {
                rdst[j] = ry[j] * rsrc[j];
            }
        }

        // leading z component

        auto rdst = tensor.data(iTensorTwoPosition + curdim - 1);

        auto rsrc = tensor.data(iTensorOnePosition + lowdim - 1);

        #pragma omp simd aligned(rz, rdst, rsrc: VLX_ALIGN)
        for (int32_t i = 0; i < ndim; i++)
        {
            rdst[i] = rz[i] * rsrc[i];
        }
    }
}

}  // namespace genfunc

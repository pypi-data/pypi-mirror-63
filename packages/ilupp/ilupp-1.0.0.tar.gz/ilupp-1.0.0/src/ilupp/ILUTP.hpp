#pragma once

#include "declarations.h"

namespace iluplusplus {

//bool ILUTP_new(const matrix_sparse<T>& A, matrix_sparse<T>& U, index_list& perm, Integer max_fill_in, Real threshold, Integer& zero_pivots);

// ILUTP is the standard implemenation. Accessing elements of w in increasing
// order is slow. This is improved in ILUTP2 using vector_sparse_dynamic_enhanced

template<class T>
void ILUTP2(
        const matrix_sparse<T>& A, matrix_sparse<T>& L, matrix_sparse<T>& U, index_list& perm,
        Integer max_fill_in, Real threshold, Real piv_tol, Integer bp,
        Integer& zero_pivots, Real& time_self, Real mem_factor)
{
    if(non_fatal_error(!A.square_check(),"matrix_sparse::ILUTP2: argument matrix must be square."))
        throw iluplusplus_error(INCOMPATIBLE_DIMENSIONS);
    const Integer m = A.rows(), n = A.columns();

    const clock_t time_begin = clock();
    // the notation will be for A being a ROW matrix, i.e. U and L also ROW matrices

    if(max_fill_in<1) max_fill_in = 1;
    if(max_fill_in>n) max_fill_in = n;

    Integer k,i,j,p;
    zero_pivots=0;
    vector_sparse_dynamic_enhanced<T> w(m);
    index_list list_L, list_U;

    perm.resize(n);
    index_list inverse_perm(n);

    const Integer reserved_memory = min(max_fill_in*n, (Integer) mem_factor*A.non_zeroes());
    U.reformat(m,m,reserved_memory,ROW);
    L.reformat(m,m,reserved_memory,ROW);

    // (1.) begin for i
    for(i=0;i<n;i++){
        if (i == bp)
            piv_tol = 1.0;     // always pivot

        // (2.) initialize w to A[i,:], compute norm of lower part
        Real norm_wL = 0.0;
        for(k=A.pointer[i]; k<A.pointer[i+1]; k++){
            j = inverse_perm[A.indices[k]];
            w(A.indices[k], j) = A.data[k];
            if (j < i)
                norm_wL += absvalue_squared(A.data[k]);
        }
        norm_wL = std::sqrt(norm_wL);

        w.move_to_beginning();
        while(w.current_sorting_index() < i && !w.at_end()){
            if (std::abs(w.current_element()) < threshold*norm_wL){
                w.current_zero_set();
                // taking a step forward is not necessary, because the iterator
                // jumps automatically ahead if current element is erased.
            } else {
                k = w.current_sorting_index();
                const T wk = (w.current_element() /= U.data[U.pointer[k]]);
                for (j = U.pointer[k]+1; j<U.pointer[k+1]; j++) {
                    w(U.indices[j], inverse_perm[U.indices[j]]) -= wk * U.data[j];
                } // end for
                w.take_step_forward();
            }   // end if
        } // end while

        // (10.) Do dropping in w.
        // NB: The dropping criterion for U is slightly different than in
        // standard ILUT because the norm also takes the diagonal entry into
        // account (which can never be dropped in ILUT).
        w.take_largest_elements_by_abs_value_with_threshold(
                list_L, list_U, inverse_perm, max_fill_in-1, max_fill_in,
                threshold, threshold, i, piv_tol);
        // we need one element less for L, as the diagonal will always be 1.
        if(list_U.dimension()==0) {
            // no nonzero pivot found - try again without threshold for U
            if (threshold > 0.0)
                w.take_largest_elements_by_abs_value_with_threshold(
                        list_L, list_U, inverse_perm, max_fill_in-1, max_fill_in,
                        threshold, 0.0, i);
                // we need one element less for L, as the diagonal will always be 1.

            if (list_U.dimension() == 0) {
                zero_pivots++;
                w(perm[i],i) = 1.0;
                list_U.resize(1);
                list_U[0] = perm[i];
            }
        }

        // (11.) Copy values to L:
        if(L.pointer[i]+list_L.dimension()+1>reserved_memory)
            throw std::runtime_error("ILUTP2: memory reserved was insufficient.");

        for (j=0; j<list_L.dimension(); j++) {
            L.data[L.pointer[i]+j] = w[list_L[list_L.dimension()-1-j]];
            L.indices[L.pointer[i]+j] = inverse_perm[list_L[list_L.dimension()-1-j]];
        }
        // write 1 to the diagonal
        L.data[L.pointer[i]+list_L.dimension()]=1.0;
        L.indices[L.pointer[i]+list_L.dimension()]=i;

        L.pointer[i+1]=L.pointer[i]+list_L.dimension()+1;

        // (12.) Copy values to U:
        if (U.pointer[i] + list_U.dimension() > reserved_memory)
            throw std::runtime_error("ILUTP2: memory reserved was insufficient.");

        // write them in opposite order so the largest (pivoting) element comes first
        for(j=0; j<list_U.dimension(); j++){
            U.data[U.pointer[i]+j] = w[list_U[list_U.dimension()-1-j]];
            U.indices[U.pointer[i]+j] = list_U[list_U.dimension()-1-j];
        }
        U.pointer[i+1]=U.pointer[i]+list_U.dimension();

        // perform pivoting
        p = inverse_perm[U.indices[U.pointer[i]]];
        inverse_perm.switch_index(perm[i], U.indices[U.pointer[i]]);
        perm.switch_index(i, p);
        if(U.data[U.pointer[i]]==0)
            throw std::runtime_error("matrix_sparse::ILUTP2: encountered zero pivot in row ");

        // (13.) w:=0
        w.zero_reset();
    }  // (14.) end for i

    L.compress();
    U.compress();

    U.reorder(inverse_perm);
    L.normal_order();

    time_self=((Real)clock() - (Real)time_begin)/(Real)CLOCKS_PER_SEC;
}

} // end namespace iluplusplus

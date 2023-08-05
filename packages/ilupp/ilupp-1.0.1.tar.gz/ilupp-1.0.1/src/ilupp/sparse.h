/***************************************************************************
 *   Copyright (C) 2006 by Jan Mayer                                       *
 *   jan.mayer@mathematik.uni-karlsruhe.de                                 *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/


#ifndef SPARSE_H
#define SPARSE_H

#include <new>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstdlib>
#include <ctime>
#include <iomanip>
#include <cmath>
#include <stack>
#include <map>
#include <queue>
#include <vector>
#include <complex>

#include "declarations.h"

#include "arrays.h"
#include "functions.h"
#include "parameters.h"
#include "orderings.h"



// Scalar-Product does not include complex conjugation, needs to be adapted for complex numbers
// Hence, currently the scalar product, norm2, norm2squared,norm2_along_orientation, etc. are incorrect for complex numbers.

namespace iluplusplus {

template<class T> class vector_dense
   {
       private:
           Integer size;
           T* data;
           bool non_owning = false;

           friend class matrix_sparse<T>;
       public:
        // constructors & destructors
           vector_dense();
           vector_dense(Integer m);
           vector_dense(Integer m, T t);
           vector_dense(const vector_dense& x);
           vector_dense(Integer m, T* _data, bool _non_owning=false);
           ~vector_dense();
       // Basic functions
           void scale(T d);    // (*this)=d*(*this)
           void scale(T d, const vector_dense<T>& v); // (*this)=d*v
           void add(T d);    // (*this)=d+(*this)(elementwise) 
           void add(T d, const vector_dense<T>& v); // (*this)=v+d (elementwise) 
           void power(Real c); // calculates |*this|^c
           void scale_at_end(const vector_dense<T>& v);  // scales *this with v at the end, v being shorter than *this
           void scale_at_end_and_project(const vector_dense<T>& v, const vector_dense<T>& scale); // scales v with scales at the end, scales being shorter than v; *this is the final scaled part.
           void inverse_scale_at_end(const vector_dense<T>& v);  // same as above, except the inverses are used
           void inverse_scale_at_end_and_project(const vector_dense<T>& v, const vector_dense<T>& scale);
           void add(const vector_dense<T> &v);                                                           // (*this)=v+w
           void subtract(const vector_dense<T> &v);                                                           // (*this)=v+w
           void multiply(const vector_dense<T> &v); // by elements                                                          // (*this)=v+w
           T product() const;                       // returns product of all elements.
           void divide(const vector_dense<T> &v);   // by elements                                                        // (*this)=v+w
           void invert();
           void invert(const vector_dense<T> &v);
           void add_scaled(T alpha, const vector_dense<T> &v);                                         // (*this)=(*this)+alpha*v
           void scale_add(T alpha, const vector_dense<T> &v);                                          // (*this)=alpha*(*this)+v
           void vector_addition(const vector_dense<T> &v, const vector_dense<T> &w);                     // (*this)=v+w
           void scaled_vector_addition(const vector_dense<T> &v, T alpha, const vector_dense<T> &w);     // (*this)=v+alpha*w
           void scaled_vector_addition(T alpha, const vector_dense<T> &v, const vector_dense<T> &w);     // (*this) = alpha*v +w
           void scaled_vector_subtraction(T alpha, const vector_dense<T> &w, const vector_dense<T> &v);     // (*this)=alpha*w-v
           void vector_subtraction(const vector_dense<T> &v, const vector_dense<T> &w);                  // (*this)=v-w
           void residual(matrix_usage_type use, const matrix_sparse<T> &A, const vector_dense<T> &x, const vector_dense<T> &b); // (*this)=b-Ax  or  (*this)=b-(A^T)*x
           void extract(const matrix_sparse<T> &A, Integer m);   // (*this) is the m-th row or column of A having the same orienattion.
           void extract_from_matrix_update(T d, const matrix_sparse<T> &A, Integer k);          // (*this)=d*A[k]+(*this), where A[k] is either the k-th row or column, depending on the orientation of A.
           void extract(const vector_dense<T>& x,Integer begin,Integer end);         // extracts vector from x, begin (and including) begin, and ending (but excluding) end.
       // Operators
           vector_dense<T> operator +(vector_dense const &v) const;
           vector_dense<T> operator -(vector_dense const &v) const;
           vector_dense<T> operator *(T k) const;                    // multiplication with a scalar
           T operator *(const vector_dense &v) const;          // scalar product
       // Functions, Manipulation, Information
           Integer dimension() const;
           Integer dim() const;
           void print_info() const;
           void absvalue();                                    // overwrites the vector with its absolute value, elementwise
           void absvalue(const vector_dense<T>& v);            // (*this) contains the absolute values of v elementwise.
           void absvalue(const vector_dense<T>& v, Integer begin, Integer n);            // (*this) contains the absolute values of v elementwise, starting at beginning, with size n.
           void absvalue(const T* values, Integer begin, Integer n);  // *this will have the size n and will contain the absolute value of the elements of values.
           Real norm1() const;
           Real norm2() const;
           Real norm2_squared() const;
           Real norm_max() const;
           bool zero_check(Integer k);
           void shortest_vector_point_line(const vector_dense<T>& r, const vector_dense<T>& p, const vector_dense<T>& t); // returns shortest vector in 2-norm
           // connecting r with the line x = p + (lambda)t, lambda\in T (i.e. the line through p in the direction of t)
           Real distance_point_to_line(const vector_dense<T>& p, const vector_dense<T>& t) const;
           // returns distance in 2-norm of *this to the line x = p + (lambda)t, lambda\in T (i.e. the line through p in the direction of t)
      // Accessing elements
           T get(Integer j) const;
           T& operator[](Integer j);
           const T& operator[](Integer j) const;
           T& set(Integer j);
       // Assignment
           vector_dense<T>& operator =(const vector_dense<T>& x);        // Assignment
           void copy_and_destroy(vector_dense<T>& v); // *this = v; v is destroyed in the process (i.e. becomes a vector of dimension 0)
           void interchange(vector_dense<T>& v);      // interchanges (swaps) *this and v
           void interchange(T*& newdata, Integer& newsize);
        // vector_dense-valued operators
           void switch_entry (Integer i, Integer j); // switches elements having indices i and j respectively.
       // Sorting
           void sort(index_list& list, Integer left, Integer right, Integer m);
           // chooses m largest elements from left to right,including left and right.
           // and places indices in list. In doing so, *this is rearanged. The m largest elements (or the indices respectively)
           // will be contained in the indices right-m+1..right.
           void quicksort(index_list& list, Integer left, Integer right);
           void quicksort(index_list& list);

           // vector_dense<T> permute(const index_list& perm);
           void insert(const vector_dense<T>& b, Integer position, T value);
           // this is constructed as follows: inserts value at position into b.
           void insert_at_end(const vector_dense<T>& v);
           // permute this vector according to perm
           void permute(const index_list& perm);
           // assign the permutation of x according to perm to this vector
           void permute(const vector_dense<T>& x, const index_list& perm);
           void permute_at_end(const index_list& perm);
           void permute_at_end(const vector_dense<T>& x, const index_list& perm);
       // generating special vectors
           void unitvector(Integer j);
           void set_all(T d);
           void set_natural_numbers();
           void norm2_of_dim1(const matrix_sparse<T>& A, orientation_type o);  // if o==ROW, a vector containing the norms of all rows of A is returned.
           void norm1_of_dim1(const matrix_sparse<T>& A, orientation_type o);  // if o==ROW, a vector containing the norms of all rows of A is returned.
           void erase_resize_data_field(Integer newsize);
           void resize(Integer newsize);
           void resize(Integer newsize, T d);
           void resize_set_natural_numbers(Integer newsize);
           void resize_without_initialization(Integer newsize);
           Real memory() const;
   };



// The following class allows quick setting to zero of a sparse vector, inserting non-zero elements anywhere, reading any particular element and reading all elements (but in no particular order)
// needed for all ILU-type preconditioners

 template<class T> class vector_sparse_dynamic
   {
       protected:
           Integer size;
           Integer nnz;
           std::vector<T> data;
           std::vector<Integer> occupancy;
           std::vector<Integer> pointer;
           void erase_resize_data_fields(Integer m);
       public:
        // constructors & destructors
           vector_sparse_dynamic();
           vector_sparse_dynamic(Integer m);
           void resize(Integer m);
        // functions
           Integer dimension() const                { return size; }
           Integer non_zeroes() const               { return nnz; }
           // below, x refers to internal indices in [0,nnz), and j to actual row/column indices in [0,size)
           const T& get_data(Integer x) const       { return data[x]; }
           T& get_data(Integer x)                   { return data[x]; }
           const Integer& get_pointer(Integer x) const { return pointer[x]; }
           Integer& get_pointer(Integer x)          { return pointer[x]; }
           bool zero_check(Integer j) const         { return occupancy[j] < 0; }
           bool non_zero_check(Integer j) const     { return !zero_check(j); }
           Integer find_next_index(Integer j) const;    // find x for the entry with the next index after j; -1 if none
           void zero_set();
           void zero_reset();
           T abs_max() const;  // returns value of largest element by absolute value
           T abs_max(Integer& pos) const;
           void scale(T d); // scales
           T  operator * (const vector_sparse_dynamic<T>& y) const; // scalar product
           T scalar_product_pos_factors(const vector_sparse_dynamic<T>&y) const;  // scalar product only using positive factors
       // Accessing elements
           T read(Integer j) const;
           T& operator[](Integer j);
           // better to use read than the next function
           const T& operator[](Integer j) const;
           void zero_set(Integer j);
           void print_non_zeroes() const;
       // conversion
           vector_dense<T> expand() const;
       // Norm
           Real norm1() const;
           Real norm2() const;
           Real norm2(Integer begin, Integer end) const;    // norm only of subvector with indices in [begin, end)
           Real norm_max() const;
       // Sorting
             // selects upto n elements of the *this with relative absolute value larger than the threshold. Selecting is retricted to from..to. including from, excluding to.
           void take_largest_elements_by_abs_value_with_threshold(index_list& list, Integer n, Real tau, Integer from, Integer to) const;

            // selects upto n elements of the *this with relative absolute value larger than the threshold. Chooses new pivot, permutes only if piv_tol acceptable
           void take_largest_elements_by_abs_value_with_threshold_pivot_last(index_list& list, Integer n, Real tau, Integer pivot_position, Real piv_tol) const;

             // selects upto n_L elements and upto n_U elements using threshold. Results are stored in list_L and list_U
             // respectively. An element with index i is put in list_L if invperm[i]<mid, else in list_U.
             // The last index in list_L and list_U corresponds to the largest element.
           void take_largest_elements_by_abs_value_with_threshold(index_list& list_L, index_list& list_U, const index_list& invperm, Integer n_L, Integer n_U, Real tau_L,  Real tau_U, Integer mid) const;
             // same as above, but with pivoting tolerance for U.
           void take_largest_elements_by_abs_value_with_threshold(index_list& list_L, index_list& list_U, const index_list& invperm, Integer n_L, Integer n_U, Real tau_L,  Real tau_U, Integer mid, Real piv_tol) const;

             // same as above, with selection done by weight.
           void take_single_weight_largest_elements_by_abs_value_with_threshold(const iluplusplus_precond_parameter& IP, index_list& list, Real weight, Integer n, Real tau, Integer from, Integer to) const;
           void take_single_weight_largest_elements_by_abs_value_with_threshold(const iluplusplus_precond_parameter& IP, index_list& list, index_list& rejected_list, Real weight, Integer n, Real tau, Integer from, Integer to) const;
           void take_single_weight_largest_elements_by_abs_value_with_threshold_pivot_last(index_list& list, vector_dense<Real>& weights, Integer n, Real tau, Integer pivot_position, Real piv_tol) const;

           void take_single_weight_pos_drop_largest_elements_by_abs_value_with_threshold(const iluplusplus_precond_parameter &IP, index_list& list, Real weight, Integer n, Real tau, Integer from, Integer to, Integer vector_index, Integer max_pos_drop) const;
           void take_single_weight_pos_drop_largest_elements_by_abs_value_with_threshold(const iluplusplus_precond_parameter &IP, index_list& list, index_list& rejected_list, Real weight, Integer n, Real tau, Integer from, Integer to, Integer vector_index, Integer max_pos_drop) const;

           void take_single_weight_bw_largest_elements_by_abs_value_with_threshold(const iluplusplus_precond_parameter &IP, index_list& list, Real weight, Integer n, Real tau, Integer from, Integer to, Integer vector_index,Integer bandwidth, Integer max_pos_drop) const;
           void take_single_weight_bw_largest_elements_by_abs_value_with_threshold(const iluplusplus_precond_parameter &IP, index_list& list, index_list& rejected_list, Real weight, Integer n, Real tau, Integer from, Integer to, Integer vector_index,Integer bandwidth, Integer max_pos_drop) const;

           void take_single_weight_weighted_largest_elements_by_abs_value_with_threshold(const iluplusplus_precond_parameter &IP, index_list& list, const vector_dense<Real>& weights, Real weight, Integer n, Real tau, Integer from, Integer to) const;
           void take_single_weight_weighted_largest_elements_by_abs_value_with_threshold(const iluplusplus_precond_parameter &IP, index_list& list, index_list& rejected_list, const vector_dense<Real>& weights, Real weight, Integer n, Real tau, Integer from, Integer to) const;
             // same as above, with selection done by weight.

           Real memory() const;
   };

// same as vector_sparse_dynamic, but allows sequential access to indices via a heap-based priority queue
template <class T>
class vector_sparse_ordered : public vector_sparse_dynamic<T>
{
private:
    using vector_sparse_dynamic<T>::size;
    using vector_sparse_dynamic<T>::nnz;
    using vector_sparse_dynamic<T>::data;
    using vector_sparse_dynamic<T>::occupancy;
    using vector_sparse_dynamic<T>::pointer;

    struct IndexComparator
    {
        const vector_sparse_ordered* me;

        IndexComparator(const vector_sparse_ordered& _me)
            : me(&_me)
        { }

        bool operator()(Integer x, Integer y) {
            // keep entries in ascending index order
            return me->get_pointer(x) > me->get_pointer(y);
        }
    };
    IndexComparator index_comparator;

    std::vector<Integer> index_heap;

public:
    vector_sparse_ordered() :
        vector_sparse_dynamic<T>(), index_comparator(*this)
    { }

    vector_sparse_ordered(Integer m) :
        vector_sparse_dynamic<T>(m), index_comparator(*this)
    { }

    void zero_set() {
        vector_sparse_dynamic<T>::zero_set();
        index_heap.clear();
    }
    void zero_reset() {
        vector_sparse_dynamic<T>::zero_reset();
        index_heap.clear();
    }

    void zero_set(Integer j) {
        vector_sparse_dynamic<T>::zero_set(j);
        // there is no good way to remove the index from the index_heap, but it's ok;
        // it will just come up as a numeric zero
    }

    T& operator[](Integer j) {
        if (occupancy[j] < 0) {
            occupancy[j]=nnz;
            pointer[nnz]=j;
            nnz++;
            data[occupancy[j]] = static_cast<T>(0);

            // update the priority queue
            index_heap.push_back(nnz-1);
            std::push_heap(index_heap.begin(), index_heap.end(), index_comparator);
        }
        return data[occupancy[j]];
    }

    Integer pop_next_index() {
        if (index_heap.empty())
            return -1;
        else {
            std::pop_heap(index_heap.begin(), index_heap.end(), index_comparator);
            const Integer x = index_heap.back();
            index_heap.pop_back();
            return x;
        }
    }
};


// same as vector_sparse_dynamic, but all non-zero elements can be accessed by increasing indices -- needed for ILUTP

template<class T> class vector_sparse_dynamic_enhanced  : public vector_sparse_dynamic<T>
  {
       protected:
           std::map <Integer, Integer> key;
           std::map <Integer, Integer>::iterator current_position_iter;
           // avoid using: the first function does not update the key, the second requires user to have COMPATIBLE arguments j and k, but this is not checked.
           // better to use: current_zero_set
           void zero_set(Integer j);    // sets element with index j to zero, but does not remove element from key
           void zero_set(Integer j, Integer k); // sets element with index j having sorting index k to zero.
       public:
        // constructors & destructors
           vector_sparse_dynamic_enhanced();
           vector_sparse_dynamic_enhanced(Integer m);
           vector_sparse_dynamic_enhanced(const vector_sparse_dynamic_enhanced& x);
           void resize(Integer m);
       // Assignment
           vector_sparse_dynamic_enhanced<T>& operator =(const vector_sparse_dynamic_enhanced<T>& x);        // Assignment
           void zero_set();
           void zero_reset();
           T read(Integer j) const;
           T& operator()(Integer j, Integer k);   // returns a reference for an element at position j with sorting order k.
           T& operator[](Integer j);    // does not set sorting index!!! do not use if not initialized
           void current_zero_set(); // sets current element to zero.
           void move_to_beginning();
           Integer& current_index();    // returns the current index of the vector entry
           Integer& current_position(); // returns the position in pointer that points to the appropriate data element
           Integer current_sorting_index() const; // returns the current index for sorting purposes
           T& current_element();  // returns the current value
           void take_step_forward();
           bool at_beginning() const;
           bool at_end() const;
           Real memory() const;
  };


template<class T> class matrix_sparse
{
    public:
        // these are public so that ILU* algorithms can access them directly
        T* data;
        Integer* pointer;
        Integer* indices;
        orientation_type orientation;
    private:
        Integer number_rows;
        Integer number_columns;
        Integer nnz;
        Integer pointer_size;
        bool non_owning = false;     // if true, data won't be freed in the destructor

           void insert_data(const vector_dense<T>& data_vector, const index_list& list, Integer begin_index);
             // copies the indices from list into indices and the data stored in data_vector corresponding to the appropriate indices into data.
           void insert_data(const vector_dense<T>& data_vector, const index_list& list, Integer begin_index_matrix, Integer begin_index_list, Integer n, Integer offset=0);
             // copies the indices from list into indices and data stored in data_vector into data. n data elements are copied, beginning in list at begin_index_list, insertion beginning at begin_index_matrix. Indices in matrix are offset by offset vs vector indices.
           void erase_resize_data_fields(Integer new_nnz);                                      // replaces indices and data with the new size new_nnz
           void erase_resize_pointer_field(Integer new_pointer_size);                               // replaces pointer field with the new size new_pointer_size (but does not adjust orientation, row or column size.)
           void erase_resize_all_fields(Integer new_pointer_size, Integer new_nnz);    // replaces all fields with new sized fields
           Integer largest_absolute_value_along_orientation(Integer k) const; // returns the position in data of the largest element in a row/column by absolute value (row if ROW matrix, column if COLUMN matrix).
           void sum_absolute_values_along_orientation(vector_dense<Real> &v) const;                          // calculates the row sum of abs. values for row oriented matrices, vice versa for column
           void sum_absolute_values_against_orientation(vector_dense<Real> &v) const;                        // calculates the column sum of abs. values for row matrices and vice versa
           void vector_of_matrix_matrix_multiplication(const matrix_sparse<T>& C, Integer i, vector_dense<T>& result, orientation_type o) const;
           void row_of_matrix_matrix_multiplication(const matrix_sparse<T>& C, Integer i, vector_dense<T>& result) const;
           void column_of_matrix_matrix_multiplication(const matrix_sparse<T>& C, Integer i, vector_dense<T>& result) const;
             // the previous functions stores the i-th row/column of (*this)*C as a dense vector in result.
           void keepFillin(const matrix_sparse<T> &m, Integer fillin,  matrix_sparse<T>& n) const;
           void generic_matrix_vector_multiplication_addition(matrix_usage_type use, const vector_dense<T>& x, vector_dense<T>& v) const;  // v=v+(*this)*x or v=v+(*this)^T*x, no error handling, hence private
           void enlarge_fields_keep_data(Integer newnnz);
           // NOTE: The following routines are somewhat dangerous to use as they circumvent the private data of this class. They should be used with great care.
           // uses the pointers indicated to setup a matrix. No memory is allocated.
           // These routines have not been tested!!!
           void setup(Integer m, Integer n, Integer nonzeroes, T* data_array, Integer* indices_array, Integer* pointer_array, orientation_type O);
           // sets matrix to a (0,0) matrix and returns the information needed to free the data           
           void free(Integer& m, Integer& n, Integer& nonzeroes, Integer& ps, T*& data_array, Integer*& indices_array, Integer*& pointer_array, orientation_type& O);
           // sets matrix to a (0,0) matrix, but frees no memory. You still have be able to access the data somehow to free it....
           void null_matrix_keep_data();

       public:
        // constructors, destructors
           matrix_sparse();
           matrix_sparse(orientation_type o, Integer m, Integer n);      // does not allocate memory, as nnz is unknown
           matrix_sparse(orientation_type o, Integer m, Integer n, Integer nz); // allocates memory
           matrix_sparse(const matrix_sparse& X);   // copy constructor
           matrix_sparse(matrix_sparse&& X);        // move constructor
           ~matrix_sparse();
           matrix_sparse(T* _data, Integer* _indices, Integer* _pointer, Integer _rows, Integer _columns, orientation_type _orientation, bool _non_owning=false);

           // assignment operator
           matrix_sparse& operator= (matrix_sparse<T> X);

        // Basic functions
           T get_data(Integer k) const;
           Integer get_index(Integer k) const;
           Integer get_pointer(Integer k) const;
           Integer get_pointer_size() const;
           T& set_data(Integer k);
           Integer& set_index(Integer k);
           Integer& set_pointer(Integer k);

           // matrix is reformatted to contain a new number of rows, columns, non-zero elements, and new orientation. The various fields are adjusted appropriately, but are NOT initialized.
           void reformat(Integer new_number_rows, Integer new_number_columns, Integer new_nnz, orientation_type new_orientation);

           bool square_check() const;
           void matrix_vector_multiplication_add(matrix_usage_type use, const vector_dense<T>& x, vector_dense<T>& v) const;             // v=v+(*this)*x
           void matrix_vector_multiplication(matrix_usage_type use, const vector_dense<T>& x, vector_dense<T>& v) const;                 // v=(*this)*x
           void matrix_vector_multiplication(matrix_usage_type use, vector_dense<T>& v) const;                 // v=(*this)*x
           // void matrix_transpose_vector_multiplication_add(const vector_dense<T>& x, vector_dense<T>& v) const;   // v=v+(*this^T)*x
           // void matrix_transpose_vector_multiplication(const vector_dense<T>& x, vector_dense<T>& v) const;       // v=(*this^T)*x
           void matrix_matrix_multiplication(T beta, const matrix_sparse<T>& B, const matrix_sparse<T>& C, orientation_type result_orientation, Real matrix_density); // calculates beta*A*C and drops elements to ensure orientationwise the density specified
           void matrix_addition(T alpha, const matrix_sparse<T>& A, const matrix_sparse<T>& B);
             // calculates (*this) = alpha*A + B.
             // note: the size of the fields for the sum will be the sum of the field sizes of A and B.
           matrix_sparse<T> transpose_in_place();  // transposes the matrix itself, and destroys original matrix, i.e. orientation and sizes are switched
           Real row_density() const;
           Real column_density() const;
           void scalar_multiply(T d);  // multiplies matrix itself with d (and overwrites it)

           // append a row (or column in the CSC case) containing of the entries of w indexed by row_indices
           void append_row(Integer i, const vector_sparse_dynamic<T>& w, const std::vector<Integer>& row_indices);
           // append first the single prefix entry and then an indexed row (or column in the CSC case)
           void append_row_with_prefix(Integer i, const vector_sparse_dynamic<T>& w, const std::vector<Integer>& row_indices, Integer prefix_j, T prefix_value);
           // append an indexed row (or column in the CSC case) and then the single suffix entry
           void append_row_with_suffix(Integer i, const vector_sparse_dynamic<T>& w, const std::vector<Integer>& row_indices, Integer suffix_j, T suffix_value);

           //////////////////////////////////////////////
           // scaling the rows and columns of matrices //
           //////////////////////////////////////////////

           // multiply the o's with the entries of v
           void scale(const vector_dense<T>& v, orientation_type o);
           // scale rows with D1, columns with D2
           void scale(const vector_dense<T>& D1, const vector_dense<T>& D2);
           // scale with D1 along orientation, with D2 against
           void scale_orientation_based(const vector_dense<T>& D1, const vector_dense<T>& D2);

           // divide the o's with the entries of v
           void inverse_scale(const vector_dense<T>& v, orientation_type o);
           // scale rows with 1/D1, columns with 1/D2
           void inverse_scale(const vector_dense<T>& D1, const vector_dense<T>& D2);
           // scale with 1/D1 along orientation, with 1/D2 against
           void inverse_scale_orientation_based(const vector_dense<T>& D1, const vector_dense<T>& D2);

           void normalize_columns(vector_dense<T>& D_r);
           void normalize_rows(vector_dense<T>& D_l);
           void normalize();
           void normalize(vector_dense<T>& D_l, vector_dense<T>& D_r);
           bool numerical_zero_check(Real threshold) const; // returns true, if Frobenius norm is less than threshold.
           void insert_orient(const matrix_sparse<T> &A, const vector_dense<T>& along_orient, const vector_dense<T>& against_orient, T center, Integer pos_along_orient, Integer pos_against_orient, Real threshold);
           // inserts all elements in along_orient, against_orient, center whose abs. value is larger than threshold.
           // along_orientation is inserted at the position indicated in the same orientation as the matrix
           // against_orientation is inserted at the position indicated in the opposite orientation as the matrix
           // center is inserted at the intersection of both positions
           void insert(const matrix_sparse<T> &A, const vector_dense<T>& row, const vector_dense<T>& column, T center, Integer pos_row, Integer pos_col, Real threshold);
           // inserts elements whose absolute value is larger than threshold of both a row and a column at positions indicated
        // matrix-valued operations
           matrix_sparse operator *(T d) const;        // returns matrix*d (scalar multiplication)

           // return the same as this, but with the orientation reversed (csr <-> csc)
           matrix_sparse<T> change_orientation() const;

           // returns a triangular part of the matrix - csr: lower, csc: upper
           matrix_sparse<T> natural_triangular_part(bool increasing) const;

           void interchange(matrix_sparse<T>& A); // interchanges two matrices without copying data
           void interchange(T*& Adata, Integer*& Aindices, Integer*& Apointer, Integer& Anumber_rows, Integer& Anumber_columns, orientation_type& Aorientation);
           void interchange(T*& Adata, Integer*& Aindices, Integer*& Apointer, Integer& Anumber_rows, Integer& Anumber_columns, Integer& Annz, orientation_type& Aorientation);
           void copy_and_destroy(matrix_sparse<T>& A);  // *this = A, but destroys A in the process, i.e. A becomes an empty matrix. Copying is done efficiently by pointers, not elements
        // vector_dense-valued operators
           vector_dense<T> operator *(const vector_dense<T>& x) const; // matrix-vector-multiplication
        // Information
           Integer rows() const;                       // returns the number of rows.
           Integer columns() const;                    // returns the number of columns.
           Integer dim_along_orientation() const;      // returns the dimension in the direction of the orientation, i.e. the number of rows for row matrix and number of colums for a column matrix.
           Integer dim_against_orientation() const;    // returns the dimension in the direction opposite to the orientation, i.e. the number of columns for a row matrix and vice versa.
           Integer dim_major() const { return pointer_size - 1; }       // dimension along the major axis, i.e., number of rows for CSR
           Integer dim_minor() const { return dim_against_orientation(); } // dimension along the minor axis, i.e., number of cols for CSR
           Integer dimension() const;                  // returns number of rows. In DEBUG modus, points out that matrix is not square.
           Integer bandwidth() const;
           Integer max_one_dim_size() const;                  // returns maximal size needed to store a row for ROW matrix, a column for COLUMN matrix.
           Integer read_pointer_size() const;
           Integer read_pointer(Integer i) const;
           Integer read_index(Integer i) const;
           T read_data(Integer i)const;
           orientation_type orient() const;        // returns the orientation of *this.
           Integer non_zeroes() const;        // returns the number of non-zeroes of *this. i.e. the reserved memory.
           Integer actual_non_zeroes() const; // returns the actual number of non-zeroes, i.e. the used memory.
        // Functions
           Real norm1() const;    // 1-norm of matrix
           Real normF() const;
           Real norm_max() const;
           T scalar_product_along_orientation(Integer m, Integer n) const; // calculates the scalar product (*this)[m] * (*this)[n], (*this)[i] being the i-th row or column.
        // Conversion
           //matrix_dense<T> expand() const;   // converts the matrix to a dense_matrix
           void compress(double threshold=0.0);    // removes those elements, whose absolute value is less than threshold.
           void positional_compress(const iluplusplus_precond_parameter& IP, double threshold=0.0);    // removes those elements, whose absolute value is less than threshold and weighs with position.
           //void compress(const matrix_dense<T>& A, orientation_type o, double threshold);
        // Generating special matrices
           void diag(T d);    //makes diagonal matrix, keeping the size.
           void diag(Integer m, Integer n, T d, orientation_type o); // makes a matrix having m rows, n columns of orientation o having d on the diagonal.
           void square_diag(Integer n, T d, orientation_type o);    // same as above only square
           void tridiag (T a, T b, T c); // makes a tridiagonal SQUARE matrix
           void read_binary(std::string filename);
           void write_binary(std::string filename) const;
           void extract(const matrix_sparse<T> &A, Integer m, Integer n); // *this will contain the rows/columns m to m+n-1 of A - determined by orientation.
        // Testing
           bool check_consistency() const;
           void print_pointer() const;
           void print_indices() const;
           void print_data() const;
           void print_orientation() const;
           void print_info() const;
           void print_detailed_info() const;
           void print_all() const;
           //Real degree_of_symmetry() const;
           special_matrix_type shape() const;
        // Interaction with systems of linear equations
           void lower_triangular_solve(const vector_dense<T>& b, vector_dense<T>& x) const;
           void upper_triangular_solve(const vector_dense<T>& b, vector_dense<T>& x) const;
           void triangular_solve(special_matrix_type form, matrix_usage_type use, const vector_dense<T>& b, vector_dense<T>& x) const;
           void triangular_solve(special_matrix_type form, matrix_usage_type use, vector_dense<T>& x) const;
           void triangular_solve_perm(special_matrix_type form, matrix_usage_type use, const index_list& perm, const vector_dense<T>& b, vector_dense<T>& x) const;
           void triangular_solve_perm(special_matrix_type form, matrix_usage_type use, const index_list& perm, vector_dense<T>& x) const;
           void triangular_solve_with_smaller_matrix(special_matrix_type form, matrix_usage_type use, vector_dense<T>& x) const; // solve is performed for bottom part of matrix
           void triangular_solve_with_smaller_matrix_permute_first(special_matrix_type form, matrix_usage_type use, const index_list& perm, vector_dense<T>& x) const;
           //not needed // void triangular_solve_with_smaller_matrix_permute_first_return_small(special_matrix_type form, matrix_usage_type use, const index_list& perm, vector_dense<T>& x) const;
           void triangular_solve_with_smaller_matrix_permute_last(special_matrix_type form, matrix_usage_type use, const index_list& perm, vector_dense<T>& x) const;
           void triangular_drop(special_matrix_type form, const matrix_sparse<T>& M, Integer max_fill_in, Real tau);
           // drops (non-pivot) elements in a triangular matrix, keeping pivots in place as well as the order of the other elements,
           // but dropping those with rel. size less than tau, keeping at most fill_in.
           // dropping is done along the orienation of the matrix.
           void weighted_triangular_drop_against_orientation(special_matrix_type form, const matrix_sparse<T>& M, const vector_dense<T> weights, Integer max_fill_in, Real tau);
           // same as above, but drops using weights and in the direction of the orienation of the matrix, i.e. for e ROW matrix, dropping is done by rows.
           void weighted_triangular_drop(special_matrix_type form, const matrix_sparse<T>& M, const vector_dense<T> weights, orientation_type o, Integer max_fill_in, Real tau);
           // same as above, dropping is done along orienation o.
           void expand_kernel(const matrix_sparse<T>& A, const vector_dense<T>& b, const vector_dense<T>& c, T beta, T gamma, Integer row_pos, Integer col_pos);           void weighted_triangular_drop_along_orientation(special_matrix_type form, const matrix_sparse<T>& M, const vector_dense<T> weights, Integer max_fill_in, Real tau);
           // *this is the matrix (A x | y^T z) such that (b | beta) is in the kernel of A and (c | gamma) is in the kernel of A^T.
           // beta and gamma must be non-zero. x,y,z are chosen appropriately. 
           // Actual insertion of additonal row and column is done at the position indicated by row_pos, col_pos
           void expand_kernel(const matrix_sparse<T>& A, const vector_dense<T>& b, const vector_dense<T>& c, T beta, T gamma, Integer row_pos, Integer col_pos, vector_dense<T>& bnew, vector_dense<T>& cnew);
           void regularize(const matrix_sparse<T>& A,const vector_dense<T>& b, const vector_dense<T>& c, T d,Integer row_pos, Integer col_pos); // insert a column b, a row c at positions indicated in attempt to increase rank by 2
           void regularize_with_rhs(const matrix_sparse<T>& A,const vector_dense<T>& b, const vector_dense<T>& c, T d,Integer row_pos, Integer col_pos, const vector_dense<T>& old_rhs, vector_dense<T>& new_rhs);  // same as above, but yields new rhs
           // Preconditioners
           // ILUCP
           // ILUCP: standard implementation, ILUCPinv: implementation with inverse dropping; old implementations have slow access for L
           // cfh: disabled because it doesn't compile
           // same as ILUCP4 only with inverse-based dropping
           //bool ILUCP4inv(const matrix_sparse<T>& Acol, matrix_sparse<T>& U, index_list& perm, Integer max_fill_in, Real threshold, Real piv_tol, Integer rp, Integer& zero_pivots, Real& time_self, Real mem_factor = 10.0);
           bool ILUCDP(const matrix_sparse<T>& Arow, const matrix_sparse<T>& Acol, matrix_sparse<T>& U, index_list& perm, index_list& permrows, Integer max_fill_in, Real threshold, Real piv_tol, Integer bpr, Integer& zero_pivots, Real& time_self, Real mem_factor = 6.0);
           // cfh: disabled because it doesn't compile
           //bool ILUCDPinv(const matrix_sparse<T>& Arow, const matrix_sparse<T>& Acol, matrix_sparse<T>& U, index_list& perm, index_list& permrows, Integer max_fill_in, Real threshold, Real piv_tol, Integer bpr, Integer& zero_pivots, Real& time_self, Real mem_factor = 6.0);
           // pivots rows and columns, rows based on number of elements in row of L; possibly with inverse based dropping.
           bool partialILUC(const matrix_sparse<T>& Arow, matrix_sparse<T>& Anew, const iluplusplus_precond_parameter& IP, bool force_finish, matrix_sparse<T>& U, vector_dense<T>& Dinv, Integer last_row_to_eliminate, Real threshold, Integer& zero_pivots, Real& time_self, Real mem_factor, Real& total_memory_allocated, Real& total_memory_used);
           bool partialILUCDP(const matrix_sparse<T>& Arow, const matrix_sparse<T>& Acol, matrix_sparse<T>& Anew, const iluplusplus_precond_parameter& IP, bool force_finish, matrix_sparse<T>& U, vector_dense<T>& Dinv, index_list& perm, index_list& permrows, index_list& inverse_perm, index_list& inverse_permrows,Integer last_row_to_eliminate, Real threshold, Integer bp,  Integer bpr,  Integer epr, Integer& zero_pivots, Real& time_self, Real mem_factor, Real& total_memory_allocated, Real& total_memory_used);
           bool preprocessed_partialILUCDP(const iluplusplus_precond_parameter& IP, bool force_finish, const matrix_sparse<T>& A, matrix_sparse<T>& Acoarse, matrix_sparse<T>& U, vector_dense<T>& Dinv, index_list& permutation_rows, index_list& permutation_columns, index_list& inverse_permutation_rows, index_list& inverse_permutation_columns, vector_dense<T>& D_l, vector_dense<T>& D_r, Real threshold, Integer& zero_pivots, Real& setup_time, Real mem_factor, Real& total_memory_allocated, Real& total_memory_used);
        // sorting algorithms
#ifdef ILUPLUSPLUS_USES_SPARSPAK
           void rcm(); // performs rcm on *this
           void rcm(const matrix_sparse<T>& A); // performs rcm on A and stores result in *this
           void rcm(index_list& P) const; // returns permuation needed to perform rcm on *this
           void rcm(index_list& P, Integer b, Integer e) const; // returns permuation needed to perform rcm on *this; begins at i=b and ends at i<e
#endif
           Integer ddPQ(index_list& P, index_list& Q, Real tau) const;
           Integer ddPQ_dyn_av(index_list& P, index_list& Q, Real tau) const;
           Integer symm_ddPQ_dyn_av(index_list& P, index_list& Q, Real tau) const;
           Integer choose_ddPQ(const iluplusplus_precond_parameter& IP,index_list& P, index_list& Q) const;
           Integer ddPQ(index_list& P, index_list& Q, Integer from, Integer to, Real tau) const;
           void test_ordering(index_list& P, index_list& Q) const; // a routine to test orderings
           bool maximal_weight_inverse_scales(index_list& P, vector_dense<T>& D1, vector_dense<T>& D2) const;  // returns inverse of scaling factors
#ifdef ILUPLUSPLUS_USES_METIS
           void metis_node_nd(index_list& P, index_list& invP) const;
           void metis_node_nd(Integer* P, Integer* invP) const;
#endif
#ifdef ILUPLUSPLUS_USES_PARDISO
           int pardiso_maximal_weight(int* P, double* D1, double* D2) const;  // returns natural logarithm of scaling factors
           int pardiso_maximal_weight(index_list& P, vector_dense<T>& D1, vector_dense<T>& D2) const;  // returns scaling factors
           int pardiso_maximal_weight_inverse_scales(index_list& P, vector_dense<T>& D1, vector_dense<T>& D2) const;  // returns inverse of scaling factors
           int solve_pardiso(const vector_dense<T>& b, vector_dense<T>& x,int& peak_memory, int& perm_memory, int& nnzLU, double& solve_time) const;
#endif
           void unit_or_zero_diagonal(vector_dense<T>& D1) const; // D1 contains a vector with entries 0 +/- 1 s.t. the scaled matrix along orientation has a nonnegative diagonal

           // preprocess as indicated by L; returns first index where preprocessing was not successful
           Integer preprocess(const iluplusplus_precond_parameter& IP, index_list& P, index_list& Q, index_list& invP, index_list& invQ, vector_dense<T>& Drow, vector_dense<T>& Dcol);

           bool test_I_matrix() const; // requires element w/ absolute value 1 on diagonal and elements with absolute value of no more than 1 otherwise.
           bool test_normalized_I_matrix() const; // also requires 1 on diagonal
           Real test_diag_dominance(Integer i) const; // test diagonal dominance along orientation of a single row i or column i.
           Real test_diag_dominance() const; //  max of test above
           void reorder(const index_list& invperm);     // the indices of *this will be in the order of perm , invperm = perm^{-1}
           matrix_sparse<T> normal_order();   // the indices are sorted in ascending order for each row/column.
           void permute(const matrix_sparse<T>& A, const index_list& perm); // permutes A along orientation and returns permuted matrix
           void permute_against_orientation(const matrix_sparse<T>& A, const index_list& perm);// permutes A against own orientation and returns permuted matrix
           void permute_against_orientation_with_invperm(const matrix_sparse<T>& A, const index_list& invperm); 
           void permute_along_and_against_orientation(const matrix_sparse<T>& A, const index_list& perm_along, const index_list& perm_against);
           void permute_along_with_perm_and_against_orientation_with_invperm(const matrix_sparse<T>& A, const index_list& perm_along, const index_list& invperm_against);
           void permute(const matrix_sparse<T>& A, const index_list& perm, orientation_type O); // permutes A along orientation indicated and returns permuted matrix
           void permute(const matrix_sparse<T>& A, const index_list& permP, const index_list& permQ); // permutes rows of A with Pperm, columns of A with Qperm.
           void permute(const matrix_sparse<T>& A, const index_list& permP, const index_list& permQ, const index_list& invpermP, const index_list& invpermQ); // same as abvove, but faster.
           void permute(const index_list& perm, orientation_type O); // permutes *this as indicated.
           void permute(const index_list& permP, const index_list& permQ); // permutes *this as indicated.
           void permute(const index_list& permP, const index_list& permQ, const index_list& invpermP, const index_list& invpermQ);
           void permute_efficiently(matrix_sparse<T>& H, const index_list& permP, const index_list& permQ, const index_list& invpermP, const index_list& invpermQ); // H is a help-matrix (work space), contains original matrix *this after permuting
           void permute_efficiently(matrix_sparse<T>& H, const index_list& permP, const index_list& permQ); // H is a help-matrix (work space), contains original matrix *this after permuting

           ////////////////////
           // PQ permutation //
           ////////////////////

           // apply ddPQ to a matrix and returns permuted matrix
           Integer ddPQ(matrix_sparse<T>& A, orientation_type PQorient, Real tau);
           // apply ddPQ to a matrix and returns permuted matrix
           Integer ddPQ(matrix_sparse<T>& A, orientation_type PQorient, Integer from, Integer to, Real tau);
           // apply ddPQ to a matrix and vector and returns permuted matrix and vector
           Integer ddPQ(matrix_sparse<T>& A, const vector_dense<T>& bold, vector_dense<T>& bnew, orientation_type PQorient, Real tau);
           // apply ddPQ to a matrix and vector and returns permuted matrix and vector
           Integer ddPQ(matrix_sparse<T>& A, const vector_dense<T>& bold, vector_dense<T>& bnew, orientation_type PQorient, Integer from, Integer to, Real tau);
           // symmetrized PQ (P=Q) for I-matrices
           void sym_ddPQ(index_list& P) const;
           // apply ddPQ to a matrix and vector and returns permuted matrix and vector
           Integer multilevel_PQ(matrix_sparse<T>& A, const vector_dense<T>& bold, vector_dense<T>& bnew, orientation_type PQorient, Integer& level, Real tau);

           void sparse_first_ordering(index_list& Q) const;  // moves sparse columns of a row matrix to the beginning
           void symmetric_move_to_corner(index_list& P) const; // returns a permutation P, that moves elements into corners by absolute value (1-norm) |a_(k,:)| + |a_(:,k)|
           void symmetric_move_to_corner_improved(index_list& P) const; // same as above, but only considers the the appropriate k x k block in step k
           void symb_symmetric_move_to_corner(index_list& P) const; // returns a permutation P, that moves elements into corners by #elements #(a_(k,:)) + #(a_(:,k))
           void symb_symmetric_move_to_corner_improved(index_list& P) const; // same as above, only considers k x k block in k-th step
           void weighted_symmetric_move_to_corner(index_list& P) const; // weighs with number of elements of both k-th row and column together
           void weighted_symmetric_move_to_corner_improved(index_list& P) const;
           void weighted2_symmetric_move_to_corner(index_list& P) const; // weighs with number of elements of both k-th row and column separately
           void weighted2_symmetric_move_to_corner_improved(index_list& P) const;
           void sp_symmetric_move_to_corner(index_list& P) const; // returns a permutation P, that moves elements into corners by scalar product a_(k,:)^T * a_(:,k)
           void sp_symmetric_move_to_corner_improved(index_list& P) const; // returns a permutation P, that moves elements into corners by scalar product a_(k,:)^T * a_(:,k)
           void diagonally_dominant_symmetric_move_to_corner_improved(index_list& P) const; // returns a permutation P, that moves elements into corners by scalar product by absolute value, but produces a diagonally dominant initial block
           Real memory() const;
 };



class index_list
  {
       private:
           std::vector<Integer> indices;
       public:
           index_list();
           index_list(Integer _size);
           index_list(Integer _size, Integer _reserved);
           std::vector<Integer>& vec()              { return indices; }
           const std::vector<Integer>& vec() const  { return indices; }
           Integer dimension() const    { return indices.size(); }
           size_t size() const          { return indices.size(); }
           Integer memory_used() const;
           Integer find(Integer k) const; // returns -1 if k is not found in list, else the position of k.
           void resize(Integer newsize);
           void resize(Integer newsize, Integer new_memory);
           void resize_without_initialization(Integer newsize);
           void resize_without_initialization(Integer newsize, Integer new_memory);
           void resize_with_constant_value(Integer newsize, Integer d);
           void switch_index(Integer i,Integer j);   // switch indices having index i and j
           Integer& operator[](Integer j);
           const Integer& operator[](Integer j) const;
           void interchange(index_list& A);
           void print_info() const;
           void init(); // initializes list with 0,..,size-1
           void init(Integer n);   // initializes first n elements only.
           void init(Integer n, Integer begin); // initializes first n elements from begin,...begin+n-1.
           void quicksort(Integer left, Integer right); // sorts list from index left to right.

           // sorts list from index left to right. If invperm is inverse prior
           // to sorting, then it is inverse after sorting as well.
           void quicksort_with_inverse(index_list& invperm, Integer left, Integer right);

           void quicksort(index_list& list, Integer left, Integer right);
           index_list permute(const index_list& perm);
           void permute(const index_list& x, const index_list& perm);
           //friend void matrix_sparse<T>::insert_data(const vector_dense<T>& data_vector, const index_list& list, Integer begin_index);
           // assign the inverse of the permutation perm to this list
           void invert(const index_list& perm);
           void reflect(const index_list& perm);
           void compose(const index_list& P, const index_list& Q);
           void compose(const index_list& P);
           void compose_left(const index_list& P);
           void compose_right(const index_list& P);
           bool ID_check() const;
           bool check_if_permutation() const;
           Real memory() const;
           // returns the number of indices that are equal
           Integer equality(const index_list& v) const;
           Integer equality(const index_list& v, Integer from, Integer to) const;
           // returns the number of indices that are equal divided by the number of indices considered.
           Real relative_equality(const index_list& v) const;
           Real relative_equality(const index_list& v, Integer from, Integer to) const;
  };


/*********************************************************************/
// Other Declarations
/*********************************************************************/

template<class T> T scalar_prod(const matrix_sparse<T> &A, Integer m, const matrix_sparse<T> &B, Integer n);

template<class T> std::istream& operator >> (std::istream& is, vector_dense<T> &x);
template<class T> std::ostream& operator << (std::ostream& os, const vector_dense<T> &x);
template<class T> std::ostream& operator << (std::ostream& os, const matrix_sparse<T> & x);
std::ostream& operator << (std::ostream& os, const index_list& x);

void quicksort(index_list& v, index_list& list, const index_list& permutation, Integer left, Integer right);
void quicksort(index_list& v, const index_list& permutation, Integer left, Integer right);

#ifdef ILUPLUSPLUS_USES_PARDISO // requires: libpardiso
    extern "C" {int mps_pardiso(int, int, int, int*, int*, double*, int*, double*, double*, int);
                int pardiso_solve(int n, int* ia, int* ja, double* a, double* b, double* x, int mtype, int* peak_memory, int* perm_memory, int* nnzLU, double* time);
    }
#endif

} // end namespace iluplusplus

#endif




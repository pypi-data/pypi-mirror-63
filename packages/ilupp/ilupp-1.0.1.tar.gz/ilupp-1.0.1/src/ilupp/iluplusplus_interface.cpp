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

#include "iluplusplus.h"
#include "iluplusplus_interface.h"

namespace iluplusplus {

bool solve_with_multilevel_preconditioner(const matrix& A, const vector& b, const vector& x_exact, vector& x, bool exact_solution_known,
          Real& eps_rel_residual, Real& abs_residual, Integer& max_iter_iterations_used, Real& abs_error,
          std::string directory, std::string matrix_name, const iluplusplus_precond_parameter &IP, bool detailed_output, std::string directory_data){
    try {
        bool success;
        Real time = 0.0;
        if(detailed_output) success = solve_with_multilevel_preconditioner_with_detailed_output<Coeff_Field,matrix,vector>(A,b,x_exact,x,exact_solution_known,eps_rel_residual,abs_residual,max_iter_iterations_used,abs_error,time,directory,matrix_name,directory_data,IP);
        else success = solve_with_multilevel_preconditioner<Coeff_Field,matrix,vector>(A,b,x_exact,x,exact_solution_known,eps_rel_residual,abs_residual,max_iter_iterations_used,abs_error,time,directory,matrix_name,IP);
        return success;
    }
    catch(iluplusplus_error ippe){
        std::cerr<<"solve_with_multilevel_preconditioner: "<<ippe.error_message()<<std::endl;
        throw;
    }
}


bool solve_with_multilevel_preconditioner(Integer n, Integer nnz, orientation_type O, Coeff_Field*& data, Integer*& indices, Integer*& pointer,  Coeff_Field*& b, Integer& n_x_exact, Coeff_Field*& x_exact,  Integer& n_x, Coeff_Field*& x, bool exact_solution_known,
          Real& eps_rel_residual, Real& abs_residual, Integer& max_iter_iterations_used, Real& abs_error,
          std::string directory, std::string matrix_name, const iluplusplus_precond_parameter &IP, bool detailed_output, std::string directory_data){
    try {
        bool success;
        matrix Amat;
        vector bvec,xvec,x_exactvec;
        Integer nc = n;
        Integer nr = n;
        Integer n_b = n;
        Amat.interchange(data,indices,pointer,nr,nc,nnz,O);
        bvec.interchange(b,n_b);
        xvec.interchange(x,n_x);
        x_exactvec.interchange(x_exact,n_x_exact);
        Real time = 0.0;
        if(detailed_output) success = solve_with_multilevel_preconditioner_with_detailed_output<Coeff_Field,matrix,vector>(Amat,bvec,x_exactvec,xvec,exact_solution_known,eps_rel_residual,abs_residual,max_iter_iterations_used,abs_error,time,directory,matrix_name,directory_data,IP);
        else success = solve_with_multilevel_preconditioner<Coeff_Field,matrix,vector>(Amat,bvec,x_exactvec,xvec,exact_solution_known,eps_rel_residual,abs_residual,max_iter_iterations_used,abs_error,time,directory,matrix_name,IP);
        Amat.interchange(data,indices,pointer,nr,nc,nnz,O);
        bvec.interchange(b,n_b);
        xvec.interchange(x,n_x);
        x_exactvec.interchange(x_exact,n_x_exact);
        return success;
    }
    catch(iluplusplus_error ippe){
        std::cerr<<"solve_with_multilevel_preconditioner: "<<ippe.error_message()<<std::endl;
        throw;
    }
}

bool solve_with_multilevel_preconditioner(orientation_type O, const std::vector<Coeff_Field>& data_vec, const std::vector<Integer>& indices_vec, const std::vector<Integer>& pointer_vec, const std::vector<Coeff_Field>& b_vec, const std::vector<Coeff_Field>& x_exact_vec, std::vector<Coeff_Field>& x_vec, bool exact_solution_known,
          Real& eps_rel_residual, Real& abs_residual, Integer& max_iter_iterations_used, Real& abs_error,
          std::string directory, std::string matrix_name, const iluplusplus_precond_parameter &IP, bool detailed_output, std::string directory_data){
    try {
        bool success;
        Integer n = pointer_vec.size()-1;
        if( non_fatal_error( data_vec.size() != indices_vec.size(), "solve_with_multilevel_preconditioner: data_vec and indices_vec need to have same dimension.")) throw iluplusplus_error(INCOMPATIBLE_DIMENSIONS);
        if(non_fatal_error(b_vec.size() != pointer_vec.size()-1 ||  x_vec.size() != pointer_vec.size()-1,"solve_with_multilevel_preconditioner: b_vec and x_vec need to have same dimension, pointer_vec dimension + 1.")) throw iluplusplus_error(INCOMPATIBLE_DIMENSIONS);
        if(non_fatal_error(exact_solution_known && x_exact_vec.size() != pointer_vec.size()-1,"solve_with_multilevel_preconditioner: exact solution is known, but has wrong dimension.")) throw iluplusplus_error(INCOMPATIBLE_DIMENSIONS);
        Integer nnz = pointer_vec[n]; 
        if(x_vec.size() != pointer_vec.size()-1) x_vec.resize(pointer_vec.size()-1);
        // these casts are needed to pass the pointers to ILU++ data types. However, the data will not be manipulated.
        Coeff_Field* data     = const_cast<Coeff_Field*>(&data_vec[0]);
        Integer* indices      = const_cast<Integer*>(&indices_vec[0]);
        Integer* pointer      = const_cast<Integer*>(&pointer_vec[0]);
        Coeff_Field* b        = const_cast<Coeff_Field*>(&b_vec[0]);
        Coeff_Field* x_exact  = const_cast<Coeff_Field*>(&x_exact_vec[0]);
        Coeff_Field* x        = &x_vec[0];
        Integer n_x_exact     = x_exact_vec.size();
        Integer n_x           = x_vec.size();
        success = solve_with_multilevel_preconditioner(n,nnz,O,data,indices,pointer,b,n_x_exact,x_exact,n_x,x,exact_solution_known,eps_rel_residual,abs_residual,max_iter_iterations_used,abs_error,directory,matrix_name,IP,detailed_output,directory_data);
        return success;
    }
    catch(iluplusplus_error ippe){
        std::cerr<<"solve_with_multilevel_preconditioner: "<<ippe.error_message()<<std::endl;
        throw;
    }
}

}  // end namespace iluplusplus

/* do not edit automatically generated by mc from MathLib0.  */
/* MathLib0.def provides access to math functions.

Copyright (C) 2003-2020 Free Software Foundation, Inc.
Contributed by Gaius Mulley <gaius.mulley@southwales.ac.uk>.

This file is part of GNU Modula-2.

GNU Modula-2 is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3, or (at your option)
any later version.

GNU Modula-2 is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

Under Section 7 of GPL version 3, you are granted additional
permissions described in the GCC Runtime Library Exception, version
3.1, as published by the Free Software Foundation.

You should have received a copy of the GNU General Public License and
a copy of the GCC Runtime Library Exception along with this program;
see the files COPYING3 and COPYING.RUNTIME respectively.  If not, see
<http://www.gnu.org/licenses/>.  */


#if !defined (_MathLib0_H)
#   define _MathLib0_H

#   ifdef __cplusplus
extern "C" {
#   endif
#   if !defined (PROC_D)
#      define PROC_D
       typedef void (*PROC_t) (void);
       typedef struct { PROC_t proc; } PROC;
#   endif


#   if defined (_MathLib0_C)
#      define EXTERN
#   else
#      define EXTERN extern
#   endif

#   define MathLib0_pi 3.1415926535897932384626433832795028841972
#   define MathLib0_exp1 2.7182818284590452353602874713526624977572
EXTERN double MathLib0_sqrt (double x);
EXTERN double MathLib0_exp (double x);
EXTERN double MathLib0_ln (double x);
EXTERN double MathLib0_sin (double x);
EXTERN double MathLib0_cos (double x);
EXTERN double MathLib0_tan (double x);
EXTERN double MathLib0_arctan (double x);
EXTERN int MathLib0_entier (double x);
#   ifdef __cplusplus
}
#   endif

#   undef EXTERN
#endif
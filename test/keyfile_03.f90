!-----------------------------------------------------------------------------
!
! Evaluation of the PDF of a gamma distribution
!
! This Fortran code is translated from the C code in /src/nmath of that comes
! with version 3.1 of the statistical programming language 'R':
!
!-----------------------------------------------------------------------------
!
!  AUTHOR
!    Catherine Loader, catherine@research.bell-labs.com.
!    October 23, 2000.
!
!  Merge in to R:
!  Copyright (C) 2000 The R Core Team
!  Copyright (C) 2004 The R Foundation
!
!  This program is free software; you can redistribute it and/or modify
!  it under the terms of the GNU General Public License as published by
!  the Free Software Foundation; either version 2 of the License, or
!  (at your option) any later version.
!
!  This program is distributed in the hope that it will be useful,
!  but WITHOUT ANY WARRANTY; without even the implied warranty of
!  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
!  GNU General Public License for more details.
!
!  You should have received a copy of the GNU General Public License
!  along with this program; if not, a copy is available at
!  http://www.r-project.org/Licenses/
!
!
! DESCRIPTION
!
!   Computes the density of the gamma distribution,
!
!                   1/s (x/s)^{a-1} exp(-x/s)
!        p(x;a,s) = -----------------------
!                            (a-1)!
!
!   where `s' is the scale (= 1/lambda in other parametrizations)
!     and `a' is the shape parameter ( = alpha in other contexts).
!
!  The old (R 1.1.1) version of the code is available via `#define D_non_pois'

function dgam (x, shape, scale, give_log) result(fn_val)  !ThIsIsAtEsT

   implicit none

   double precision, intent(in) :: x, shape, scale

   logical(kind = 4) :: give_log

   double precision, parameter :: pos_inf = 1.0e99
   double precision, parameter :: neg_inf = -1.0e99
   double precision, parameter :: nan = 9999.0

   double precision :: pr, dpois_raw, fn_val

   if (shape .lt. 0.0 .or. scale .le. 0.0) then
      print *, ' Invalid shape or scale parameter in "dgamma", NaN returned!'  !ThIsIsAtEsT
      fn_val = nan
   endif

   if (x .lt. 0.0) then
      if (give_log) then
         fn_val = neg_inf
      else
         fn_val = 0.0
      endif
      return
   endif

   if (shape .eq. 0.0) then  ! point mass at 0
      if (x .eq. 0.0) then
         fn_val = pos_inf
      else
         if (give_log) then
            fn_val = neg_inf
         else
            fn_val = 0.0
         endif
      endif
      return
   endif

   if (x .eq. 0.0) then
      if (shape .lt. 1.0) then
         fn_val = pos_inf
      else if (shape .gt. 1.0) then
         if (give_log) then
            fn_val = neg_inf
         else
            fn_val = 0.0
         endif
      else
         if (give_log) then
            fn_val = - log(scale)
         else
            fn_val = 1.0 / scale
         endif
      endif
      return
   endif

   if (shape .lt. 1.0) then
      pr = dpois_raw (shape, x / scale, give_log)
      if (give_log) then
         fn_val = pr + log(shape / x)
      else
         fn_val = pr * shape / x
      endif
   else  ! shape >= 1
      pr = dpois_raw(shape - 1.0, x / scale, give_log)
      if (give_log) then
         fn_val = pr - log(scale)
      else
         fn_val = pr / scale
      endif
   endif

   return

end function dgam

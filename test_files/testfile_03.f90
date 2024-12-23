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


FUNCTION dgam (x, shape, scale, give_log) RESULT(fn_val) !ThIsIsAtEsT

  IMPLICIT NONE

  DOUBLE PRECISION, INTENT(IN) :: x, shape, scale

  LOGICAL, INTENT(IN) :: give_log

  DOUBLE PRECISION, PARAMETER :: POS_INF = 1.0e99
  DOUBLE PRECISION, PARAMETER :: NEG_INF = -1.0e99
  DOUBLE PRECISION, PARAMETER :: NaN = 9999.0

  DOUBLE PRECISION :: pr, dpois_raw, fn_val

  IF (shape .lt. 0.0 .or. scale .le. 0.0) THEN
     PRINT *, ' Invalid shape or scale parameter in "dgamma", NaN returned!'  !ThIsIsAtEsT
     fn_val = NaN
  END IF

  IF (x .lt. 0.0) THEN
     IF (give_log) THEN
        fn_val = NEG_INF
     ELSE
        fn_val = 0.0
     END IF
     RETURN
  END IF

  IF (shape .eq. 0.0) THEN ! point mass at 0
     IF (x .eq. 0.0) THEN
        fn_val = POS_INF
     ELSE
        IF (give_log) THEN
           fn_val = NEG_INF
        ELSE
           fn_val = 0.0
        END IF
     END IF
     RETURN
  END IF

  IF (x .eq. 0.0) THEN
     IF (shape .lt. 1.0) THEN
        fn_val = POS_INF
     ELSE IF (shape .gt. 1.0) THEN
        IF (give_log) THEN
           fn_val = NEG_INF
        ELSE
           fn_val = 0.0
        END IF
     ELSE
        IF (give_log) THEN
           fn_val = -log(scale)
        ELSE
           fn_val = 1.0 / scale
        END IF
     END IF
     RETURN
  END IF

  IF (shape .lt. 1.0) THEN
     pr = dpois_raw (shape, x/scale, give_log)
     IF (give_log) THEN
        fn_val = pr + log(shape/x)
     ELSE
        fn_val = pr*shape/x
     END IF
  ELSE  ! shape >= 1
     pr = dpois_raw(shape-1.0, x/scale, give_log)
     IF (give_log) THEN
        fn_val = pr - log(scale)
     ELSE
        fn_val =  pr/scale
     END IF
  END IF

  RETURN

END FUNCTION dgam

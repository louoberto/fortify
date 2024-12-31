function gam1 (a)

!*****************************************************************************80
!
!! gam1 computes 1 / gamma(a + 1) - 1 for - 0.5 < = a < = 1.5
!
!author : 
!
!armido didinato, alfred morris
!
!reference : 
!
!armido didinato, alfred morris, 
!algorithm 708 : 
!significant digit computation of the incomplete beta function ratios, 
!acm transactions on mathematical software, 
!volume 18, 1993, pages 360 - 373.
!
!parameters : 
!
!input, real (kind = 8) a, forms the argument of the gamma function.
!
!output, real (kind = 8) gam1, the value of 1 / gamma (a + 1) - 1.
!
   implicit none

   real(kind = 8) :: a
   real(kind = 8) :: bot
   real(kind = 8) :: d
   real(kind = 8) :: gam1
   real(kind = 8), parameter, dimension (7) :: p = (/ &
   0.577215664901533d+00, -0.409078193005776d+00, &
   -0.230975380857675d+00, 0.597275330452234d-01, &
   0.766968181649490d-02, -0.514889771323592d-02, &
   0.589597428611429d-03 /)
   real(kind = 8), dimension (5) :: q = (/ &
   0.100000000000000d+01, 0.427569613095214d+00, &
   0.158451672430138d+00, 0.261132021441447d-01, &
   0.423244297896961d-02 /)
   real(kind = 8), dimension (9) :: r = (/ &
   -0.422784335098468d+00, -0.771330383816272d+00, &
   -0.244757765222226d+00, 0.118378989872749d+00, &
   0.930357293360349d-03, -0.118290993445146d-01, &
   0.223047661158249d-02, 0.266505979058923d-03, &
   -0.132674909766242d-03 /)
   real(kind = 8) :: t
   real(kind = 8) :: top
   real(kind = 8) :: w
   real(kind = 8), parameter :: s1 = 0.273076135303957d+00
   real(kind = 8), parameter :: s2 = 0.559398236957378d-01

   d = a - 0.5d+00

   if (0.0d+00 .lt. d) then
      t = d - 0.5d+00
   else
      t = a
   endif

   if (t .eq. 0.0d+00) then

      gam1 = 0.0d+00

   else if (0.0d+00 .lt. t) then

      top = (((((p(7) * t + p(6)) * t + p(5)) * t + p(4)) * t + p(3)) * t + p(2)) * t + p(1)

      bot = (((q(5) * t + q(4)) * t + q(3)) * t + q(2)) * t + 1.0d+00

      w = top / bot

      if (d .le. 0.0d+00) then
         gam1 = a * w
      else
         gam1 = (t / a) * ((w - 0.5d+00) &
         -0.5d+00)
      endif

   else if (t .lt. 0.0d+00) then

      top = (((((((&
      r(9) &

      bot = (s2 * t + s1) * t + 1.0d+00
      w = top / bot

      if (d .le. 0.0d+00) then
         gam1 = a * ((w + 0.5d+00) + 0.5d+00)
      else
         gam1 = t * w / a
      endif

   endif

   return
end

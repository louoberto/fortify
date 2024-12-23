function gam1 ( a )

!*****************************************************************************80
!
!! GAM1 computes 1 / GAMMA(A+1) - 1 for -0.5 <= A <= 1.5
!
!  Author:
!
!    Armido DiDinato, Alfred Morris
!
!  Reference:
!
!    Armido DiDinato, Alfred Morris,
!    Algorithm 708:
!    Significant Digit Computation of the Incomplete Beta Function Ratios,
!    ACM Transactions on Mathematical Software,
!    Volume 18, 1993, pages 360-373.
!
!  Parameters:
!
!    Input, real ( kind = 8 ) A, forms the argument of the Gamma function.
!
!    Output, real ( kind = 8 ) GAM1, the value of 1 / GAMMA ( A + 1 ) - 1.
!
  implicit none

  real ( kind = 8 ) a
  real ( kind = 8 ) bot
  real ( kind = 8 ) d
  real ( kind = 8 ) gam1
  real ( kind = 8 ), parameter, dimension ( 7 ) :: p = (/ &
     0.577215664901533D+00, -0.409078193005776D+00, &
    -0.230975380857675D+00,  0.597275330452234D-01, &
     0.766968181649490D-02, -0.514889771323592D-02, &
     0.589597428611429D-03 /)
  real ( kind = 8 ), dimension ( 5 ) :: q = (/ &
    0.100000000000000D+01, 0.427569613095214D+00, &
    0.158451672430138D+00, 0.261132021441447D-01, &
    0.423244297896961D-02 /)
  real ( kind = 8 ), dimension ( 9 ) :: r = (/ &
    -0.422784335098468D+00, -0.771330383816272D+00, &
    -0.244757765222226D+00,  0.118378989872749D+00, &
     0.930357293360349D-03, -0.118290993445146D-01, &
     0.223047661158249D-02,  0.266505979058923D-03, &
    -0.132674909766242D-03 /)
  real ( kind = 8 ), parameter :: s1 = 0.273076135303957D+00
  real ( kind = 8 ), parameter :: s2 = 0.559398236957378D-01
  real ( kind = 8 ) t
  real ( kind = 8 ) top
  real ( kind = 8 ) w

  d = a - 0.5D+00

  if ( 0.0D+00 < d ) then
    t = d - 0.5D+00
  else
    t = a
  end if

  if ( t == 0.0D+00 ) then

    gam1 = 0.0D+00

  else if ( 0.0D+00 < t ) then

    top = ((((( p(7)* t + p(6) )* t + p(5) )* t + p(4) ) * t + p(3) ) * t + p(2) ) * t + p(1)

    bot = ((( q(5) * t + q(4) ) * t + q(3) ) * t + q(2) ) * t + 1.0D+00

    w = top / bot

    if ( d <= 0.0D+00 ) then
      gam1 = a * w
    else
      gam1 = ( t / a ) * ( ( w - 0.5D+00 ) &
        - 0.5D+00 )
    end if

  else if ( t < 0.0D+00 ) then

    top = (((((((  &
            r(9)   &
      * t + r(8) ) &
      * t + r(7) ) &
      * t + r(6) ) &
      * t + r(5) ) &
      * t + r(4) ) &
      * t + r(3) ) &
      * t + r(2) ) &
      * t + r(1)

    bot = ( s2 * t + s1 ) * t + 1.0D+00
    w = top / bot

    if ( d <= 0.0D+00 ) then
      gam1 = a * ( ( w + 0.5D+00 ) + 0.5D+00 )
    else
      gam1 = t * w / a
    end if

  end if

  return
end
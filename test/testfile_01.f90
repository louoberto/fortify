subroutine barnes_like(nx,ny,ideterm,validmask,precip_in,precip_out)
! ---------------------------------------------------------------------------------------- 
!
! ---------------------------------------------------------------------------------------- 
implicit none

! ---------------------------------------------------------------------------------------- 
! Input/Output Variables
! ---------------------------------------------------------------------------------------- 
integer, intent(in) :: nx
integer, intent(in) :: ny
integer, intent(in) :: ideterm
integer(kind=2), intent(in), dimension(nx,ny) :: validmask
real, intent(inout), dimension(nx,ny) :: precip_in
real, intent(out), dimension(nx,ny) :: precip_out

! ---------------------------------------------------------------------------------------- 
! Local Variables
! ---------------------------------------------------------------------------------------- 
integer :: i,j,k,ii,jj
integer :: imin,imax,jmin,jmax
integer :: icut
real :: dist,pavg,rlenscale,rlenscale2
real(kind=8) :: weight

integer, dimension(3) :: cutradius
real(kind=8), dimension(nx,ny) :: denom
real(kind=8), dimension(nx,ny) :: numer
real(kind=8), dimension(nx,ny) :: work

! ---------------------------------------------------------------------------------------- 
! Initialize
! ---------------------------------------------------------------------------------------- 
dist=0.0
pavg=0.0
weight=0.0
denom(:,:)=0.0
numer(:,:)=0.0

! ---------------------------------------------------------------------------------------- 
! Compute the averge of the input precipitation grid (inside validmask).
! ---------------------------------------------------------------------------------------- 
pavg=sum(precip_in*real(validmask))/sum(real(validmask))

! ---------------------------------------------------------------------------------------- 
! Perform something akin to a Barnes filtering, weighting the data by
! exp(-dist**2/lengthscale**2) this loop tallies up the numerator and denominator needed
! for weighted sum calculation.
! ---------------------------------------------------------------------------------------- 
icut=10
rlenscale=3.
rlenscale2=rlenscale**2
do j=1,ny
   jmin=max(1,j-icut)
   jmax=min(ny,j+icut)
   do i=1,nx
      imin=max(1,i-icut)
      imax=min(nx,i+icut)
      if(validmask(i,j).eq.0)then
         do jj=jmin,jmax
            do ii=imin,imax
               dist=sqrt(real((i-ii)**2+(j-jj)**2))
               weight=exp(-dist**2/rlenscale2)
               if(dist.le.icut.and.validmask(ii,jj).eq.1.and.precip_in(ii,jj).ge.0.0)then
                  numer(i,j)=numer(i,j)+weight*precip_in(ii,jj)
                  denom(i,j)=denom(i,j)+weight
               endif
            end do ! ii=imin,imax
         end do ! jj=jmin,jmax
      endif
   end do ! i=1,nx
end do ! j=1,ny

! ---------------------------------------------------------------------------------------- 
! Set the output over water to the weighted sum. Over land use original values. If at a 
! point that is too far from land to have any points counted in weight, just set the 
! value to the domain-averaged land probability.
! ---------------------------------------------------------------------------------------- 
do j=1,ny
   do i=1,nx
      if(denom(i,j).gt.0.0)then 
         precip_out(i,j)=numer(i,j)/denom(i,j) 
      else
         precip_out(i,j)=precip_in(i,j)
      endif
      if(ideterm.eq.0)then !probabilistic data, 0 to 1
         if(precip_out(i,j).lt.0.0.or.precip_out(i,j).gt.1.0)precip_out(i,j)=pavg
      else ! deterministic data >=0
         if(precip_out(i,j).lt.0.0)precip_out(i,j)=pavg
      endif
   end do
end do

return
end subroutine barnes_like

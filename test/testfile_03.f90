subroutine border_smooth(nx,ny,validmask,fcst)

implicit none

! ---------------------------------------------------------------------------------------- 
! Input/Output Variables
! ---------------------------------------------------------------------------------------- 
integer, intent(in) :: nx
integer, intent(in) :: ny
integer(kind=2), intent(in), dimension(nx,ny) :: validmask
real, intent(inout), dimension(nx,ny) :: fcst

! ---------------------------------------------------------------------------------------- 
! Local Variables
! ---------------------------------------------------------------------------------------- 
integer :: i,j,n,ii,jj
integer :: imin,imax,jmin,jmax,stencil_radius
integer :: ktr0,ktr1
real :: sum0,sum1,weight

integer, dimension(5) :: stencil_sizes

real, allocatable, dimension(:,:) :: work
real, allocatable, dimension(:,:) :: work2

! ---------------------------------------------------------------------------------------- 
! Initialize
! ---------------------------------------------------------------------------------------- 
sum0=0.0
sum1=0.0
weight=0.0
stencil_sizes=(/301,151,75,51,5/)

! ---------------------------------------------------------------------------------------- 
! Allocate work array
! ---------------------------------------------------------------------------------------- 
if(allocated(work))deallocate(work)
allocate(work(nx,ny))

! ---------------------------------------------------------------------------------------- 
! Put input fcst array into work array.
! ---------------------------------------------------------------------------------------- 
work(:,:)=fcst(:,:)

! ---------------------------------------------------------------------------------------- 
! Perform multiple passes over the grid, performing the border smooth with successively
! smaller stencils (i.e. subgrids) as given by array stencil_sizes.
! ---------------------------------------------------------------------------------------- 
write(6,fmt='(/A,I0.1,A)')" PERFORMING BORDER SMOOTHING WITH ",size(stencil_sizes)," PASSES"
do n=1,size(stencil_sizes)
   stencil_radius=(stencil_sizes(n)-1)/2
   write(6,fmt='(/5X,2(A,I0.1))')" PASS ",n,": STENCIL SIZE = ",stencil_sizes(n)

!!!!$OMP PARALLEL DO DEFAULT(SHARED) PRIVATE(J,I,IMIN,IMAX,JMIN,JMAX,KTR0,KTR1,SUM0,SUM1,WEIGHT,JJ,II) COLLAPSE(2)
   do j=1,ny
      do i=1,nx
         ! Grid point is inside the validmask. Iterate.
         if(validmask(i,j).eq.1)cycle

         ! Set stencil bounds per dimension. The following insures that we do not
         ! go beyond the bounds of the array (1:nx,1:ny).
         imin=max(1,i-stencil_radius)
         imax=min(nx,i+stencil_radius)
         jmin=max(1,j-stencil_radius)
         jmax=min(ny,j+stencil_radius)

         ! Per-iteration initialization
         ktr0=0
         ktr1=0
         sum0=0.0
         sum1=0.0
         weight=0.0

         ! Iterate over subgrid. Count and sum number of points inside and outside
          do jj=jmin,jmax
             do ii=imin,imax
               if(validmask(ii,jj).eq.0)then
                  ktr0=ktr0+1
                  sum0=sum0+fcst(ii,jj)
               elseif(validmask(ii,jj).eq.1)then
                  ktr1=ktr1+1
                  sum1=sum1+fcst(ii,jj)
               endif
            end do
         end do

         ! Check the count of validmask points
         if(ktr1.eq.0)then
            ! Subgrid is entirely outside the validmask. Use original value.
            work(i,j)=fcst(i,j)
         else
            ! Subgrid contains at least 1 validmask point, perform weighted average.
            sum0=sum0/real(ktr0)
            sum1=sum1/real(ktr1)
            weight=real(ktr1)/real(ktr0+ktr1)
            !print *,"I,J = ",i,j
            !print *,"   KTR0,KTR1,SUM = ",ktr0,ktr1,(ktr0+ktr1)
            !print *,"   WEIGHT = ",weight
            !print *,"   SUM0,SUM1 = ",sum0,sum1
            !print *,"   ORIG,NEW = ",work(i,j),((weight*sum1)+((1.0-weight)*sum0))
            work(i,j)=(weight*sum1)+((1.0-weight)*sum0)
         endif
      end do ! i=1,nx
   end do ! j=1,ny
!!!!$OMP END PARALLEL DO

end do ! n=1,size(stencil_sizes)

! ---------------------------------------------------------------------------------------- 
! Perfor 25-point smooth to the work array. work2 is the smoothed array.
! ---------------------------------------------------------------------------------------- 
if(allocated(work2))deallocate(work2)
allocate(work2(nx,ny))
call smth25(6,work,work2,nx,ny)

! ---------------------------------------------------------------------------------------- 
! Put the 25-point smoothed work array back into fcst, outside of validmask. So now,
! where validmask = 1, have quantile-mapped, SG-smoothed values and where validmask = 0,
! we have raw model, border-smoothed, 25-point smooth values.
! ---------------------------------------------------------------------------------------- 
do j=1,ny
   do i=1,nx
      if(validmask(i,j).eq.0)then
         fcst(i,j)=work2(i,j)
      elseif(validmask(i,j).eq.1)then
         fcst(i,j)=fcst(i,j)
      endif
   end do
end do

! ---------------------------------------------------------------------------------------- 
! Clean up.
! ---------------------------------------------------------------------------------------- 
if(allocated(work))deallocate(work)
if(allocated(work2))deallocate(work2)

return
end subroutine border_smooth

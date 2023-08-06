module Module_2

implicit none




contains

!........................................
subroutine f6(m1, m2, x) 

  implicit none
  integer(kind=8), value  :: m1
  integer(kind=8), value  :: m2
  real(kind=8), intent(inout)  :: x (0:,0:)
  integer(kind=8)  :: i  
  integer(kind=8)  :: j  

  x(:, :) = 0.0d0
  do i = 0_8, m1 - 1_8, 1
    do j = 0_8, m2 - 1_8, 1
      x(j, i) = 1.0d0*(2_8*i + j)




    end do

  end do

end subroutine
!........................................

!........................................
subroutine h(x) 

  implicit none
  real(kind=8), intent(inout)  :: x (0:)

  x(2_8) = 8.0d0
end subroutine
!........................................

end module
module Module_1

implicit none




contains

!........................................
subroutine f(x) 

  implicit none
  real(kind=8), intent(inout)  :: x (0:)

  x(0_8) = 2.0d0
end subroutine
!........................................

!........................................
subroutine g(x) 

  implicit none
  real(kind=8), intent(inout)  :: x (0:)

  x(1_8) = 4.0d0
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
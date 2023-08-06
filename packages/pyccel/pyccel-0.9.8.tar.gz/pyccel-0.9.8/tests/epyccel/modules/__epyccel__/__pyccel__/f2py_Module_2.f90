subroutine f6 (m1, m2, n0_x, n1_x, x) 

  use Module_2, only: mod_f6 => f6
  implicit none
  integer(kind=8), intent(in)  :: m1 
  integer(kind=8), intent(in)  :: m2 
  integer(kind=4), intent(in)  :: n0_x 
  integer(kind=4), intent(in)  :: n1_x 
  real(kind=8), intent(inout)  :: x (0:n0_x-1,0:n1_x-1)

  !f2py integer(kind=8) :: n0_x=shape(x,1)
  !f2py integer(kind=8) :: n1_x=shape(x,0)
  !f2py intent(c) x
  call mod_f6(m1,m2,x)
end subroutine

subroutine h (n0_x, x) 

  use Module_2, only: mod_h => h
  implicit none
  integer(kind=4), intent(in)  :: n0_x 
  real(kind=8), intent(inout)  :: x (0:n0_x-1)

  call mod_h(x)
end subroutine
subroutine f (n0_x, x) 

  use Module_1, only: mod_f => f
  implicit none
  integer(kind=4), intent(in)  :: n0_x 
  real(kind=8), intent(inout)  :: x (0:n0_x-1)

  call mod_f(x)
end subroutine

subroutine g (n0_x, x) 

  use Module_1, only: mod_g => g
  implicit none
  integer(kind=4), intent(in)  :: n0_x 
  real(kind=8), intent(inout)  :: x (0:n0_x-1)

  call mod_g(x)
end subroutine

subroutine h (n0_x, x) 

  use Module_1, only: mod_h => h
  implicit none
  integer(kind=4), intent(in)  :: n0_x 
  real(kind=8), intent(inout)  :: x (0:n0_x-1)

  call mod_h(x)
end subroutine
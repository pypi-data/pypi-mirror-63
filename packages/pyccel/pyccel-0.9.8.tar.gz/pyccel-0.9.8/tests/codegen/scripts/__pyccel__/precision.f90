
program prog_precision

implicit none

integer(kind=4) :: x2  
integer(kind=8) :: x1  
real(kind=8) :: y3  
real(kind=8) :: y1  
real(kind=4) :: y2  
integer(kind=8) :: x3  
complex(kind=8) :: z1  
complex(kind=8) :: z3  
complex(kind=4) :: z2  











x1 = Int(6_8, 8)
x2 = Int(6_8, 4)
x3 = Int(6_8, 8)
y1 = Real(6_8, 8)
y2 = Real(6_8, 4)
y3 = Real(6_8, 8)
z1 = cmplx(6_8, 0.0d0, 8)
z2 = cmplx(6_8, 0.0d0, 4)
z3 = cmplx(6_8, 0.0d0, 8)
contains

!........................................
subroutine incr_(x) 

  implicit none
  integer(kind=8), intent(in)  :: x 



  x = x + 1_8
  contains 
  subroutine decr_(y) 

    implicit none
    integer(kind=8), intent(in)  :: y 

    y = y - 1_8
  end subroutine
end subroutine
!........................................

!........................................
function f1(x, n, m) result(y)

  implicit none
  integer(kind=8) :: y  
  integer(kind=8), intent(in)  :: x 
  integer(kind=8), intent(in)  :: n 
  integer(kind=8), intent(in)  :: m 

  y = m*(-n) + x
  return
end function
!........................................

!........................................
function f2(x, m) result(y)

  implicit none
  real(kind=8) :: y  
  real(kind=8), intent(in)  :: x 
  integer(kind=8), intent(in) , optional :: m 

  if (present(m)) then
    y = x + 1_8
  else
    y = x - 1_8
  end if
  return
end function
!........................................

end program prog_precision
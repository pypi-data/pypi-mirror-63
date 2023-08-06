
program prog_ex1

implicit none


!> Usage:
!
!pyccel test.py -t
!gfortran test.f90 -lblas
!./a.out


!TODO add saxpy test







call test_daxpy()
contains

!........................................
subroutine test_daxpy() 

  implicit none
  integer(kind=8) :: n  
  real(kind=8) :: sa  
  integer(kind=8) :: incx  
  real(kind=8), allocatable :: sx (:) 
  integer(kind=8) :: incy  
  real(kind=8), allocatable :: sy (:) 

  n = 5_8
  sa = 1.0d0


  incx = 1_8
  allocate(sx(0:n - 1_8))
  sx = 0.0


  incy = 1_8
  allocate(sy(0:n - 1_8))
  sy = 0.0


  sx(0) = 1.0d0
  sx(1_8) = 3.0d0
  sx(3_8) = 5.0d0


  sy(0) = 2.0d0
  sy(1_8) = 4.0d0
  sy(3_8) = 6.0d0


  call daxpy(n, sa, sx, incx, sy, incy)
end subroutine
!........................................

end program prog_ex1
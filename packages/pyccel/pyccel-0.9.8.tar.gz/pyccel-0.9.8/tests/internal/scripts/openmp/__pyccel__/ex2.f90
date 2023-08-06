
program prog_ex2

implicit none

real(kind=8), allocatable :: b (:) 
integer(kind=8) :: i  
integer(kind=8) :: n  
real(kind=8), allocatable :: a (:) 
!coding: utf-8


!This example is the python implementation of ploop.1.f from OpenMP 4.5 examples





n = 100_8


allocate(a(0:n - 1_8))
a = 0.0
allocate(b(0:n - 1_8))
b = 0.0


!$omp parallel
!$omp do
do i = 1_8, n - 1_8, 1
  b(i) = (a(i - 1_8) + a(i))/2.0d0
end do

!$omp end do  
!$omp end parallel  

end program prog_ex2
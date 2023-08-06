
program prog_ex2

implicit none

integer(kind=4) :: i  
real(kind=8), allocatable :: a (:) 
integer(kind=4) :: n  
real(kind=8), allocatable :: b (:) 
!coding: utf-8


!This example is the python implementation of ploop.1.f from OpenMP 4.5 examples





n = 100


allocate(a(0:n - 1))
a = 0.0
allocate(b(0:n - 1))
b = 0.0


!$omp parallel
!$omp do
do i = 1, n - 1, 1
  b(i) = (a(i - 1) + a(i))/2.0d0
end do

!$omp end do  
!$omp end parallel  

end program prog_ex2
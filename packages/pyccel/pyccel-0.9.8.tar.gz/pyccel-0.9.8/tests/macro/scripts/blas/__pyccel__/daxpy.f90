
program prog_daxpy

implicit none

real(kind=8) :: alpha  
real(kind=8), allocatable :: a (:) 
integer(kind=4) :: n  
real(kind=8), allocatable :: b (:) 
!TODO default value for alpha must double and not int
!right now, textx raises an error, when we pass 1.0




n = 4


allocate(a(0:n - 1))
a = 0.0
allocate(b(0:n - 1))
b = 0.0


a(0) = 2.0d0
a(1) = 3.0d0
a(2) = 4.0d0
a(3) = 5.0d0


b(0) = 5.0d0
b(1) = 4.0d0
b(2) = 9.0d0
b(3) = 2.0d0


alpha = 2.0d0



call daxpy(n, alpha, a, 1, b, 1)
print *, b

end program prog_daxpy
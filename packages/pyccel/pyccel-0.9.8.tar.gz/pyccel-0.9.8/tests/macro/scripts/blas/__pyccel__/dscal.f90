
program prog_dscal

implicit none

real(kind=8), allocatable :: a (:) 
real(kind=8), allocatable :: b (:) 
real(kind=8) :: alpha  
integer(kind=4) :: n  




n = 4


allocate(a(0:n - 1))
a = 0.0
allocate(b(0:n - 1))
b = 0.0


a(0) = 2.0d0
a(1) = 3.0d0
a(2) = 4.0d0
a(3) = 5.0d0


alpha = 2.0d0



call dscal(n, alpha, a, 1)
print *, a

end program prog_dscal
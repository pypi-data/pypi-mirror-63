
program prog_dcopy

implicit none

real(kind=8), allocatable :: a (:) 
integer(kind=4) :: n  
real(kind=8), allocatable :: b (:) 




n = 4


allocate(a(0:n - 1))
a = 0.0
allocate(b(0:n - 1))
b = 0.0


a(0) = 2.0d0
a(1) = 3.0d0
a(2) = 4.0d0
a(3) = 5.0d0



call dcopy(n, a, 1, b, 1)
print *, b

end program prog_dcopy
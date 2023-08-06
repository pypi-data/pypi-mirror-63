
program prog_dswap

implicit none

real(kind=8), allocatable :: a (:) 
real(kind=8), allocatable :: b (:) 
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


b(0) = 5.0d0
b(1) = 4.0d0
b(2) = 9.0d0
b(3) = 2.0d0


print *, '--- before swap'
print *, a
print *, b



call dswap(n, a, 1, b, 1)


print *, '--- after swap'
print *, a
print *, b

end program prog_dswap
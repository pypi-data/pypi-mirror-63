
program prog_dgemv

implicit none

real(kind=8), allocatable :: x (:) 
integer(kind=4) :: n  
real(kind=8), allocatable :: y (:) 
real(kind=8), allocatable :: a (:,:) 
real(kind=8) :: alpha  
integer(kind=4) :: m  
real(kind=8) :: beta  
!TODO - y must be optional
!- t must be optiona, default 0 (map 1 -> 'T' and 0 -> 'N')
!- default value for beta must be 0.0 and not 0






n = 4
m = 5


allocate(a(0:m - 1, 0:n - 1))
a = 0.0
allocate(x(0:m - 1))
x = 0.0
allocate(y(0:n - 1))
y = 0.0


!...
a(0, 0) = 1.0d0
a(0, 1) = 6.0d0
a(0, 2) = 11.0d0
a(0, 3) = 16.0d0


a(1, 0) = 2.0d0
a(1, 1) = 7.0d0
a(1, 2) = 12.0d0
a(1, 3) = 17.0d0


a(2, 0) = 3.0d0
a(2, 1) = 8.0d0
a(2, 2) = 13.0d0
a(2, 3) = 18.0d0


a(3, 0) = 4.0d0
a(3, 1) = 9.0d0
a(3, 2) = 14.0d0
a(3, 3) = 19.0d0


a(4, 0) = 5.0d0
a(4, 1) = 10.0d0
a(4, 2) = 15.0d0
a(4, 3) = 20.0d0
!...


!...
x(0) = 2.0d0
x(1) = 3.0d0
x(2) = 4.0d0
x(3) = 5.0d0
x(4) = 6.0d0
!...


alpha = 2.0d0
beta = 0.0d0





call dgemv('N', m, n, alpha, a, m, x, 1, 0, y, 1)
print *, y

end program prog_dgemv
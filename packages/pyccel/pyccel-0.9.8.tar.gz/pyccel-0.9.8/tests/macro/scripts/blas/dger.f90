
program prog_dger

implicit none

integer(kind=4) :: incx  
real(kind=8), allocatable :: x (:) 
real(kind=8), allocatable :: a (:,:) 
integer(kind=4) :: incy  
real(kind=8), allocatable :: y (:) 
integer(kind=4) :: m  
integer(kind=4) :: n  
real(kind=8) :: alpha  
!TODO - y must be optional






n = 4
m = 5


allocate(a(0:m - 1, 0:n - 1))
a = 0.0
allocate(x(0:m - 1))
x = 0.0
allocate(y(0:n - 1))
y = 0.0


!...
x(0) = 2.0d0
x(1) = 3.0d0
x(2) = 4.0d0
x(3) = 5.0d0
x(4) = 6.0d0
!...


!...
y(0) = 1.0d0
y(1) = -1.0d0
y(2) = 1.0d0
y(3) = -1.0d0
!...


alpha = 2.0d0
incx = 1
incy = 1





call dger(m, n, alpha, y, 1, x, 1, a, m)
print *, a

end program prog_dger

program prog_ex3

implicit none

real(kind=8), allocatable :: x (:) 
real(kind=8) :: alpha  
integer(kind=8) :: n  
integer(kind=8) :: incy  
integer(kind=8) :: incx  
integer(kind=8) :: m  
real(kind=8), allocatable :: a (:,:) 
real(kind=8), allocatable :: y (:) 




n = 4_8
m = 5_8


allocate(a(0:m - 1_8, 0:n - 1_8))
a = 0.0
allocate(x(0:m - 1_8))
x = 0.0
allocate(y(0:n - 1_8))
y = 0.0


!...
x(0) = 2.0d0
x(1_8) = 3.0d0
x(2_8) = 4.0d0
x(3_8) = 5.0d0
x(4_8) = 6.0d0
!...


!...
y(0) = 1.0d0
y(1_8) = -1.0d0
y(2_8) = 1.0d0
y(3_8) = -1.0d0
!...


alpha = 2.0d0
incx = 1_8
incy = 1_8


call dger(n, m, alpha, y, incy, x, incx, a, n)


print *, a

end program prog_ex3

program prog_ex2

implicit none

real(kind=8), allocatable :: x (:) 
real(kind=8) :: alpha  
integer(kind=8) :: n  
integer(kind=8) :: incy  
real(kind=8) :: beta  
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
a(0, 0) = 1.0d0
a(0, 1_8) = 6.0d0
a(0, 2_8) = 11.0d0
a(0, 3_8) = 16.0d0


a(1_8, 0) = 2.0d0
a(1_8, 1_8) = 7.0d0
a(1_8, 2_8) = 12.0d0
a(1_8, 3_8) = 17.0d0


a(2_8, 0) = 3.0d0
a(2_8, 1_8) = 8.0d0
a(2_8, 2_8) = 13.0d0
a(2_8, 3_8) = 18.0d0


a(3_8, 0) = 4.0d0
a(3_8, 1_8) = 9.0d0
a(3_8, 2_8) = 14.0d0
a(3_8, 3_8) = 19.0d0


a(4_8, 0) = 5.0d0
a(4_8, 1_8) = 10.0d0
a(4_8, 2_8) = 15.0d0
a(4_8, 3_8) = 20.0d0
!...


!...
x(0) = 2.0d0
x(1_8) = 3.0d0
x(2_8) = 4.0d0
x(3_8) = 5.0d0
x(4_8) = 6.0d0
!...


alpha = 2.0d0
beta = 0.0d0


incx = 1_8
incy = 1_8
call dgemv('N', n, m, alpha, a, n, x, incx, beta, y, incy)

end program prog_ex2
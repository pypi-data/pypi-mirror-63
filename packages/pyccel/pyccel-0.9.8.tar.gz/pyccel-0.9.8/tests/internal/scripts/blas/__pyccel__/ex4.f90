
program prog_ex4

implicit none

real(kind=8) :: beta  
real(kind=8) :: alpha  
integer(kind=8) :: n  
real(kind=8), allocatable :: b (:,:) 
real(kind=8), allocatable :: c (:,:) 
integer(kind=8) :: k  
integer(kind=8) :: m  
real(kind=8), allocatable :: a (:,:) 




m = 4_8
k = 5_8
n = 4_8


allocate(a(0:k - 1_8, 0:m - 1_8))
a = 0.0
allocate(b(0:n - 1_8, 0:k - 1_8))
b = 0.0
allocate(c(0:n - 1_8, 0:m - 1_8))
c = 0.0


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
b(0, 0) = 1.0d0
b(2_8, 1_8) = 1.0d0
b(1_8, 2_8) = 1.0d0
b(3_8, 3_8) = 1.0d0
b(4_8, 3_8) = 1.0d0
!...


alpha = 2.0d0
beta = 1.0d0


call dgemm('N', 'N', m, n, k, alpha, a, m, b, k, beta, c, m)


print *, c

end program prog_ex4
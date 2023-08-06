
program prog_dgemm

implicit none

real(kind=8), allocatable :: c (:,:) 
integer(kind=4) :: k  
real(kind=8), allocatable :: a (:,:) 
real(kind=8), allocatable :: b (:,:) 
real(kind=8) :: beta  
integer(kind=4) :: m  
integer(kind=4) :: n  
real(kind=8) :: alpha  
!TODO - beta, ta, tb must optional






m = 4
k = 5
n = 4


allocate(a(0:k - 1, 0:m - 1))
a = 0.0
allocate(b(0:n - 1, 0:k - 1))
b = 0.0
allocate(c(0:n - 1, 0:m - 1))
c = 0.0


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
b(0, 0) = 1.0d0
b(2, 1) = 1.0d0
b(1, 2) = 1.0d0
b(3, 3) = 1.0d0
b(4, 3) = 1.0d0
!...


alpha = 2.0d0
beta = 1.0d0





call dgemm('N', 'N', k, k, m, alpha, a, k, b, n, beta, c, n)


print *, c

end program prog_dgemm
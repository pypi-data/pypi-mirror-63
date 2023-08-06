
program prog_dgbtrf

implicit none

integer(kind=4) :: ml  
integer(kind=4) :: mu  
real(kind=8), allocatable :: a (:,:) 
integer(kind=4) :: info  
integer(kind=4) :: n  
integer(kind=4) :: m  
integer(kind=4), allocatable :: ipiv (:) 
integer(kind=4) :: lda  




n = 25
ml = 1
mu = 1
lda = 2*ml + mu + 1


allocate(a(0:lda - 1, 0:n - 1))
a = 0.0


!Superdiagonal, Diagonal, Subdiagonal
m = ml + mu
a(m - 1, 1:n - 1) = -1.0d0
a(m, 0:n - 1) = 2.0d0
a(m + 1, 0:n - 2) = -1.0d0


info = -1
allocate(ipiv(0:n - 1))
ipiv = 0





call dgbtrf(n, n, ml, mu, a, lda, ipiv, info)

end program prog_dgbtrf
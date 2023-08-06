
program prog_ex1

implicit none


!> Usage:
!
!pyccel test.py -t
!gfortran test.f90 -lblas -llapack
!./a.out


!TODO: - assert






















!assert(info == 0)

!assert(info == 0)

!assert(info == 0)

!assert(info == 0)
call test_1()
call test_2()
call test_3()
call test_4()
contains

!........................................
subroutine test_1() 

  implicit none
  integer(kind=8) :: n  
  integer(kind=8) :: ml  
  integer(kind=8) :: mu  
  integer(kind=8) :: lda  
  real(kind=8), allocatable :: a (:,:) 
  real(kind=8), allocatable :: b (:) 
  integer(kind=8) :: m  
  integer(kind=8) :: info  
  integer(kind=8), allocatable :: ipiv (:) 

  n = 25_8
  ml = 1_8
  mu = 1_8
  lda = 2_8*ml + mu + 1_8


  allocate(a(0:n - 1_8, 0:lda - 1_8))
  a = 0.0
  allocate(b(0:n - 1_8))
  b = 0.0


  b(0) = 1.0d0
  b(n - 1_8) = 1.0d0


  !Superdiagonal, Diagonal, Subdiagonal
  m = ml + mu
  a(1_8:n - 1_8, m - 1_8) = -1.0d0
  a(0:n - 1_8, m) = 2.0d0
  a(0:n - 2_8, m + 1_8) = -1.0d0


  info = -1_8
  allocate(ipiv(0:n - 1_8))
  ipiv = 0


  call dgbtrf(n, n, ml, mu, a, lda, ipiv, info)
  !assert(info == 0)


  call dgbtrs('n', n, ml, mu, 1_8, a, lda, ipiv, b, n, info)
end subroutine
!........................................

!........................................
subroutine test_2() 

  implicit none
  integer(kind=8) :: n  
  integer(kind=8) :: lda  
  real(kind=8), allocatable :: a (:,:) 
  integer(kind=8) :: info  
  integer(kind=8), allocatable :: ipiv (:) 
  integer(kind=8), allocatable :: iwork (:) 
  integer(kind=8) :: lwork  
  real(kind=8), allocatable :: work (:) 
  real(kind=8) :: anorm  
  real(kind=8) :: rcond  

  n = 3_8
  lda = n


  allocate(a(0:n - 1_8, 0:lda - 1_8))
  a = 0.0


  a(0, 0) = 0.0d0
  a(1_8, 0) = 1.0d0
  a(2_8, 0) = 2.0d0


  a(0, 1_8) = 4.0d0
  a(1_8, 1_8) = 5.0d0
  a(2_8, 1_8) = 6.0d0


  a(0, 2_8) = 7.0d0
  a(1_8, 2_8) = 8.0d0
  a(2_8, 2_8) = 0.0d0


  info = -1_8
  allocate(ipiv(0:n - 1_8))
  ipiv = 0


  call dgetrf(n, n, a, lda, ipiv, info)
  !assert(info == 0)


  allocate(iwork(0:n - 1_8))
  iwork = 0
  lwork = 4_8*n
  allocate(work(0:lwork - 1_8))
  work = 0.0


  !Get the condition number.
  anorm = 1.0d0
  rcond = -1.0d0
  call dgecon('I', n, a, lda, anorm, rcond, work, iwork, info)
end subroutine
!........................................

!........................................
subroutine test_3() 

  implicit none
  integer(kind=8) :: n  
  integer(kind=8) :: lda  
  real(kind=8), allocatable :: a (:,:) 
  integer(kind=8) :: info  
  integer(kind=8), allocatable :: ipiv (:) 
  integer(kind=8), allocatable :: iwork (:) 
  integer(kind=8) :: lwork  
  real(kind=8), allocatable :: work (:) 

  n = 3_8
  lda = n


  allocate(a(0:n - 1_8, 0:lda - 1_8))
  a = 0.0


  a(0, 0) = 0.0d0
  a(1_8, 0) = 1.0d0
  a(2_8, 0) = 2.0d0


  a(0, 1_8) = 4.0d0
  a(1_8, 1_8) = 5.0d0
  a(2_8, 1_8) = 6.0d0


  a(0, 2_8) = 7.0d0
  a(1_8, 2_8) = 8.0d0
  a(2_8, 2_8) = 0.0d0


  info = -1_8
  allocate(ipiv(0:n - 1_8))
  ipiv = 0


  call dgetrf(n, n, a, lda, ipiv, info)
  !assert(info == 0)


  allocate(iwork(0:n - 1_8))
  iwork = 0
  lwork = 4_8*n
  allocate(work(0:lwork - 1_8))
  work = 0.0


  !Compute the inverse matrix.
  call dgetri(n, a, lda, ipiv, work, lwork, info)
end subroutine
!........................................

!........................................
subroutine test_4() 

  implicit none
  integer(kind=8) :: n  
  integer(kind=8) :: lda  
  real(kind=8), allocatable :: a (:,:) 
  integer(kind=8) :: info  
  integer(kind=8), allocatable :: ipiv (:) 
  real(kind=8), allocatable :: b (:) 

  n = 3_8
  lda = n


  allocate(a(0:n - 1_8, 0:lda - 1_8))
  a = 0.0


  a(0, 0) = 0.0d0
  a(1_8, 0) = 1.0d0
  a(2_8, 0) = 2.0d0


  a(0, 1_8) = 4.0d0
  a(1_8, 1_8) = 5.0d0
  a(2_8, 1_8) = 6.0d0


  a(0, 2_8) = 7.0d0
  a(1_8, 2_8) = 8.0d0
  a(2_8, 2_8) = 0.0d0


  info = -1_8
  allocate(ipiv(0:n - 1_8))
  ipiv = 0


  call dgetrf(n, n, a, lda, ipiv, info)
  !assert(info == 0)


  !Compute the inverse matrix.
  allocate(b(0:n - 1_8))
  b = 0.0
  b(0) = 14.0d0
  b(1_8) = 32.0d0
  b(2_8) = 23.0d0


  !Solve the linear system.
  call dgetrs('n', n, 1_8, a, lda, ipiv, b, n, info)
end subroutine
!........................................

end program prog_ex1

program prog_nonblocking

use mpi
implicit none

integer(kind=4) :: rank  
integer(kind=4) :: comm  
integer(kind=4) :: tag0  
real(kind=8), allocatable :: x (:) 
integer(kind=4) :: size  
integer(kind=4) :: ierr  
integer(kind=4) :: tag1  
integer(kind=4), allocatable :: reqs (:) 
integer(kind=4) :: n  
integer(kind=4) :: prev  
real(kind=8), allocatable :: y (:) 
integer(kind=4), allocatable :: statuses (:,:) 
integer(kind=4) :: next  
!coding: utf-8

















!we need to declare these variables somehow,
!since we are calling mpi subroutines
ierr = Int(-1_8, 4)
size = Int(-1_8, 4)
rank = Int(-1_8, 4)


call mpi_init(ierr)


comm = mpi_comm_world
call mpi_comm_size(comm, size, ierr)
call mpi_comm_rank(comm, rank, ierr)


n = Int(4_8, 4)
allocate(x(0:n - 1_8))
x = 0.0
allocate(y(0:n - 1_8))
y = 0.0


if (rank == 0 ) then
  x(:) = 1.0d0
  y(:) = 2.0d0
end if
!...
tag0 = Int(1234_8, 4)
tag1 = Int(5678_8, 4)
allocate(reqs(0:3_8))
reqs = 0
!...


!...
prev = rank - 1_8
next = rank + 1_8
if (rank == 0 ) then
  prev = size - 1_8
end if
if (rank == size - 1_8 ) then
  next = 0
end if
prev = Int(prev, 4)
next = Int(next, 4)
!...


!...
call mpi_irecv(x, n, MPI_REAL8, prev, tag0, comm, reqs(0), ierr)
call mpi_irecv(y, n, MPI_REAL8, next, tag1, comm, reqs(1_8), ierr)


call mpi_isend(x, n, MPI_REAL8, prev, tag1, comm, reqs(2_8), ierr)
call mpi_isend(y, n, MPI_REAL8, next, tag0, comm, reqs(3_8), ierr)
!...


!...
allocate(statuses(0:n - 1_8, 0:mpi_status_size - 1_8))
statuses = 0
call mpi_waitall(n, reqs, statuses, ierr)
!...


call mpi_finalize(ierr)

end program prog_nonblocking
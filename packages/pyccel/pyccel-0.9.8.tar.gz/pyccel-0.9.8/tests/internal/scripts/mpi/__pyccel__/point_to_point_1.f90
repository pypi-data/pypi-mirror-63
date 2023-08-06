
program prog_point_to_point_1

use mpi
implicit none

integer(kind=4) :: source  
integer(kind=4) :: rank  
integer(kind=4) :: dest  
integer(kind=4) :: comm  
integer(kind=4) :: tag1  
integer(kind=8) :: nx  
integer(kind=4) :: size  
integer(kind=4) :: ierr  
real(kind=8), allocatable :: x (:) 
integer(kind=4) :: count  
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


nx = 4_8
allocate(x(0:nx - 1_8))
x = 0.0


if (rank == 0 ) then
  x(:) = 1.0d0
end if
source = Int(0, 4)
dest = Int(1_8, 4)


!...
tag1 = Int(1234_8, 4)
if (rank == source ) then
  x(1_8) = 2.0d0
  count = Int(1_8, 4)
  call mpi_send(x(1_8), count, MPI_REAL8, dest, tag1, comm, ierr)
  print *, "> processor ", rank, " sent x(1) = ", x
end if
!...
call mpi_finalize(ierr)

end program prog_point_to_point_1
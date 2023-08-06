
program prog_point_to_point_2

use mpi
implicit none

integer(kind=4) :: tag3  
integer(kind=4) :: source  
integer(kind=4) :: rank  
integer(kind=4), allocatable :: status (:) 
integer(kind=4) :: dest  
integer(kind=4) :: comm  
integer(kind=4) :: tag1  
integer(kind=4) :: nx  
integer(kind=4) :: size  
integer(kind=4) :: ierr  
real(kind=8), allocatable :: x (:) 
real(kind=8), allocatable :: y (:,:) 
integer(kind=4) :: tag2  
integer(kind=4) :: count  
integer(kind=4) :: ny  
integer(kind=4) :: tag5  
integer(kind=4) :: tag4  
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


nx = Int(4_8, 4)
ny = Int(2_8*3_8, 4)
allocate(x(0:nx - 1_8))
x = 0.0
allocate(y(0:1_8, 0:2_8))
y = 0.0


if (rank == 0 ) then
  x(:) = 1.0d0
  y(:, :) = 1.0d0
end if
source = Int(0, 4)
dest = Int(1_8, 4)
allocate(status(0:mpi_status_size - 1_8))
status = 0


!...
tag1 = Int(1234_8, 4)
if (rank == source ) then
  call mpi_send(x, nx, MPI_REAL8, dest, tag1, comm, ierr)
  print *, "> test 1: processor ", rank, " sent ", x
end if
if (rank == dest ) then
  call mpi_recv(x, nx, MPI_REAL8, source, tag1, comm, status, ierr)
  print *, "> test 1: processor ", rank, " got  ", x
end if
!...
!...
tag2 = Int(5678_8, 4)
count = Int(1_8, 4)
if (rank == source ) then
  x(:) = 0.0d0
  x(1_8) = 2.0d0
  call mpi_send(x(1_8), count, MPI_REAL8, dest, tag2, comm, ierr)
  print *, "> test 2: processor ", rank, " sent ", x(1_8)
end if
if (rank == dest ) then
  call mpi_recv(x(1_8), count, MPI_REAL8, source, tag2, comm, status, &
      ierr)
  print *, "> test 2: processor ", rank, " got  ", x(1_8)
end if
!...
!...
tag3 = Int(4321_8, 4)
if (rank == source ) then
  call mpi_send(y, ny, MPI_REAL8, dest, tag3, comm, ierr)
  print *, "> test 3: processor ", rank, " sent ", y
end if
if (rank == dest ) then
  call mpi_recv(y, ny, MPI_REAL8, source, tag3, comm, status, ierr)
  print *, "> test 3: processor ", rank, " got  ", y
end if
!...
!...
tag4 = Int(8765_8, 4)
count = Int(1_8, 4)
if (rank == source ) then
  y(:, :) = 0.0d0
  y(1_8, 1_8) = 2.0d0
  call mpi_send(y(1_8, 1_8), count, MPI_REAL8, dest, tag4, comm, ierr)
  print *, "> test 4: processor ", rank, " sent ", y(1_8, 1_8)
end if
if (rank == dest ) then
  call mpi_recv(y(1_8, 1_8), count, MPI_REAL8, source, tag4, comm, &
      status, ierr)
  print *, "> test 4: processor ", rank, " got  ", y(1_8, 1_8)
end if
!...
!...
tag5 = Int(6587_8, 4)
count = Int(2_8, 4)
if (rank == source ) then
  call mpi_send(y(:, 1_8), count, MPI_REAL8, dest, tag5, comm, ierr)
  print *, "> test 5: processor ", rank, " sent ", y(:, 1_8)
end if
if (rank == dest ) then
  call mpi_recv(y(:, 1_8), count, MPI_REAL8, source, tag5, comm, status, &
      ierr)
  print *, "> test 5: processor ", rank, " got  ", y(:, 1_8)
end if
!...
call mpi_finalize(ierr)

end program prog_point_to_point_2
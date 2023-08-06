
program prog_bcast
use mpi
use mpiext
implicit none

integer(kind=8), pointer :: a (:) 
integer(kind=8) :: color  
integer(kind=8) :: two  
integer(kind=8) :: key  
integer(kind=4) :: comm  
integer(kind=8) :: rank_in_world  
integer(kind=8) :: newcomm  
integer(kind=8) :: size_  
integer(kind=8) :: master  
integer(kind=8) :: m  
integer :: ierr = -1
integer, allocatable :: status (:)
call mpi_init(ierr)

allocate(status(0:-1 + mpi_status_size)) 
status = 0



size_ = -1_8
rank_in_world = -1_8


comm = mpi_comm_world
rank_in_world = mpiext_get_rank(comm)


size_ = mpiext_get_size(comm)
master = 0
m = 8_8


allocate(a(0:m-1))
a = 0


if (rank_in_world == 1_8 ) then
  a(:) = 1_8
end if
if (rank_in_world == 2_8 ) then
  a(:) = 2_8
end if
key = rank_in_world
if (rank_in_world == 1_8 ) then
  key = -1_8
end if
if (rank_in_world == 2_8 ) then
  key = -1_8
end if
two = 2_8
color = modulo(rank_in_world,two)


newcomm = -1_8


call mpi_comm_split(comm, color, key, newcomm, ierr)


!Broadcast of the message by the rank process master of
!each communicator to the processes of its group
call mpi_bcast(a, m, MPI_INTEGER8, master, newcomm, ierr)


print *, "> processor ", rank_in_world, " has a = ", a


!Destruction of the communicators
call mpi_comm_free(newcomm, ierr)




call mpi_finalize(ierr)

end program prog_bcast
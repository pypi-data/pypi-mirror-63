
program prog_split

use mpi
implicit none

integer(kind=8) :: two  
integer(kind=8), allocatable :: a (:) 
integer(kind=4) :: newcomm  
integer(kind=4) :: key  
integer(kind=4) :: c  
integer(kind=4) :: comm  
integer(kind=4) :: size  
integer(kind=4) :: ierr  
integer(kind=4) :: m  
integer(kind=4) :: master  
integer(kind=4) :: color  
integer(kind=4) :: rank_in_world  
!coding: utf-8

















!we need to declare these variables somehow,
!since we are calling mpi subroutines
ierr = Int(-1_8, 4)
size = Int(-1_8, 4)
rank_in_world = Int(-1_8, 4)


call mpi_init(ierr)


comm = mpi_comm_world
call mpi_comm_size(comm, size, ierr)
call mpi_comm_rank(comm, rank_in_world, ierr)


master = Int(0, 4)
m = Int(8_8, 4)


allocate(a(0:m - 1_8))
a = 0


if (rank_in_world == 1_8 ) then
  a(:) = 1_8
end if
if (rank_in_world == 2_8 ) then
  a(:) = 2_8
end if
key = rank_in_world
if (rank_in_world == 1_8 ) then
  key = Int(-1_8, 4)
end if
if (rank_in_world == 2_8 ) then
  key = Int(-1_8, 4)
end if
two = 2_8
c = modulo(rank_in_world,two)


color = Int(c, 4)
newcomm = Int(-1_8, 4)
call mpi_comm_split(comm, color, key, newcomm, ierr)


!Broadcast of the message by the rank process master of
!each communicator to the processes of its group
call mpi_bcast(a, m, MPI_INTEGER8, master, newcomm, ierr)


print *, "> processor ", rank_in_world, " has a = ", a


!Destruction of the communicators
call mpi_comm_free(newcomm, ierr)


call mpi_finalize(ierr)

end program prog_split
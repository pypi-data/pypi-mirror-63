
program prog_bcast

use mpi
implicit none

integer(kind=4) :: rank  
integer(kind=4) :: comm  
integer(kind=4) :: length  
integer(kind=4) :: size  
integer(kind=4) :: ierr  
integer(kind=4) :: master  
integer(kind=4) :: msg  
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


master = Int(1_8, 4)
if (rank == master ) then
  msg = rank + 1000_8
else
  msg = 0
end if
length = Int(1_8, 4)
call mpi_bcast(msg, length, MPI_INTEGER8, master, comm, ierr)


print *, 'I, process ', rank, ', received ', msg, ' from process ', master


call mpi_finalize(ierr)

end program prog_bcast
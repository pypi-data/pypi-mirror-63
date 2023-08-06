
program prog_reduce

use mpi
implicit none

integer(kind=4) :: rank  
integer(kind=8) :: sum_value  
integer(kind=4) :: comm  
integer(kind=8) :: value  
integer(kind=4) :: size  
integer(kind=4) :: ierr  
integer(kind=4) :: root  
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


root = Int(0, 4)


if (rank == 0 ) then
  value = 1000_8
else
  value = rank
end if
sum_value = 0
count = Int(1_8, 4)


call mpi_reduce(value, sum_value, count, MPI_INTEGER8, MPI_SUM, root, &
      comm, ierr)


if (rank == 0 ) then
  print *, 'I, process ', root, ', have the global sum value ', sum_value
end if
call mpi_finalize(ierr)

end program prog_reduce
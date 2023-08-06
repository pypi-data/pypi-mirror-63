
program prog_allreduce

use mpi
implicit none

integer(kind=4) :: rank  
integer(kind=8) :: value  
integer(kind=4) :: comm  
integer(kind=4) :: length  
integer(kind=4) :: size  
integer(kind=4) :: ierr  
integer(kind=8) :: product_value  
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


if (rank == 0 ) then
  value = 1000_8
else
  value = Int(rank, 4)
end if
product_value = 0
length = Int(1_8, 4)
call mpi_allreduce(value, product_value, length, MPI_INTEGER8, MPI_PROD, &
      comm, ierr)


print *, 'I, process ', rank, ', have the global product value ', product_value


call mpi_finalize(ierr)

end program prog_allreduce

program prog_allreduce
use mpi
use mpiext
implicit none

integer(kind=8) :: sum_value  
integer(kind=8) :: value  
integer(kind=4) :: comm  
integer(kind=8) :: root  
integer(kind=8) :: rank  
integer :: ierr = -1
integer, allocatable :: status (:)
call mpi_init(ierr)

allocate(status(0:-1 + mpi_status_size)) 
status = 0



!rank = -1
!we must initialize rank
comm = mpi_comm_world
rank = mpiext_get_rank(comm)


root = 0


if (rank == 0 ) then
  value = 1000_8
else
  value = rank
end if
sum_value = 0


call mpi_allreduce(value, sum_value, 1, MPI_INTEGER8, MPI_SUM, comm, &
      ierr)


print *, 'I, process ', root, ', have the global sum value ', sum_value




call mpi_finalize(ierr)

end program prog_allreduce

program prog_gather
use mpi
use mpiext
implicit none

integer(kind=8) :: i  
integer(kind=8) :: master  
integer(kind=4) :: comm  
integer(kind=8), pointer :: data (:) 
integer(kind=8), pointer :: values (:) 
integer(kind=4) :: block_length  
integer(kind=8) :: nb_values  
integer(kind=8) :: size_  
integer(kind=8) :: rank  
integer :: ierr = -1
integer, allocatable :: status (:)
call mpi_init(ierr)

allocate(status(0:-1 + mpi_status_size)) 
status = 0



!we need to declare these variables somehow,
!since we are calling mpi subroutines
size_ = -1_8
rank = -1_8
comm = mpi_comm_world
rank = mpiext_get_rank(comm)
size_ = mpiext_get_size(comm)


master = 1_8
nb_values = 8_8


block_length = floor(nb_values/Real(size_, 8))


!...
allocate(values(0:block_length-1))
values = 0
do i = 0, block_length - 1_8, 1
  values(i) = i + nb_values*rank + 1000_8


end do

print *, 'I, process ', rank, 'sent my values array : ', values
!...


!...
allocate(data(0:nb_values-1))
data = 0


call mpi_gather(values, block_length, MPI_INTEGER8, data, block_length, &
      MPI_INTEGER8, master, comm, ierr)
!...


if (rank == master ) then
  print *, 'I, process ', rank, ', received ', data, ' of process ', master
end if
call mpi_finalize(ierr)

end program prog_gather
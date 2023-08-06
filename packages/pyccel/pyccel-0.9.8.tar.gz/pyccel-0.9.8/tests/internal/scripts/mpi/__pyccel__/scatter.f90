
program prog_scatter

use mpi
implicit none

integer(kind=8), allocatable :: values (:) 
integer(kind=4) :: rank  
integer(kind=4) :: nb_values  
integer(kind=4) :: comm  
integer(kind=8), allocatable :: data (:) 
integer(kind=4) :: size  
integer(kind=4) :: ierr  
integer(kind=4) :: master  
integer(kind=4) :: block_length  
integer(kind=8) :: i  
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
nb_values = Int(8_8, 4)


block_length = floor(nb_values/Real(size, 8))


allocate(data(0:block_length - 1_8))
data = 0


if (rank == master ) then
  allocate(values(0:nb_values - 1_8))
  values = 0
  do i = 0, nb_values - 1_8, 1
    values(i) = i + 1000_8


  end do

  print *, 'I, process ', rank, ' send my values array', values
end if
call mpi_scatter(values, block_length, MPI_INTEGER8, data, block_length, &
      MPI_INTEGER8, master, comm, ierr)


print *, 'I, process ', rank, ', received ', data, ' of process ', master


call mpi_finalize(ierr)

end program prog_scatter
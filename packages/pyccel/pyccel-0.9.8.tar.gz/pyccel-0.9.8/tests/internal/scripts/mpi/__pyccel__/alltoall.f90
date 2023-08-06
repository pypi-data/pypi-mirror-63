
program prog_alltoall

use mpi
implicit none

integer(kind=8), allocatable :: values (:) 
integer(kind=4) :: rank  
integer(kind=8) :: nb_values  
integer(kind=4) :: comm  
integer(kind=8), allocatable :: data (:) 
integer(kind=4) :: size  
integer(kind=4) :: ierr  
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


nb_values = 8_8


block_length = floor(nb_values/Real(size, 8))


!...
allocate(values(0:nb_values - 1_8))
values = 0
do i = 0, nb_values - 1_8, 1
  values(i) = i + nb_values*rank + 1000_8


end do

print *, 'I, process ', rank, 'sent my values array : ', values
!...


!...
allocate(data(0:nb_values - 1_8))
data = 0


call mpi_alltoall(values, block_length, MPI_INTEGER8, data, block_length &
      , MPI_INTEGER8, comm, ierr)
!...


print *, 'I, process ', rank, ', received ', data


call mpi_finalize(ierr)

end program prog_alltoall
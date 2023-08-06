
program prog_who_am_i

use mpi
implicit none

integer(kind=4) :: size  
integer(kind=4) :: ierr  
integer(kind=4) :: rank  
integer(kind=4) :: comm  
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


print *, 'I process ', rank, ', among ', size, ' processes'


call mpi_finalize(ierr)

end program prog_who_am_i
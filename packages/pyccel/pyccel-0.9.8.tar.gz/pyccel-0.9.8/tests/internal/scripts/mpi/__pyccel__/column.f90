
program prog_column

use mpi
implicit none

integer(kind=8), allocatable :: a (:,:) 
integer(kind=4) :: source  
integer(kind=4) :: rank  
integer(kind=4), allocatable :: status (:) 
integer(kind=4) :: tag  
integer(kind=4) :: dest  
integer(kind=4) :: comm  
integer(kind=4) :: size  
integer(kind=4) :: ierr  
integer(kind=4) :: nb_lines  
integer(kind=4) :: count  
integer(kind=4) :: type_column  
integer(kind=4) :: nb_columns  
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


nb_lines = Int(3_8, 4)
nb_columns = Int(4_8, 4)
tag = Int(100_8, 4)


allocate(a(0:nb_columns - 1_8, 0:nb_lines - 1_8))
a = 0
allocate(status(0:mpi_status_size - 1_8))
status = 0


!Initialization of the matrix on each process
a(:, :) = rank + 1000_8


!Definition of the type_column datatype
type_column = Int(-1_8, 4)
  call mpi_type_contiguous(nb_lines, MPI_INTEGER8, type_column, ierr)


  !Validation of the type_column datatype
  call mpi_type_commit(type_column, ierr)


  !Sending of the first column
  if (rank == 0 ) then
    count = Int(1_8, 4)
    dest = Int(1_8, 4)
    call mpi_send(a(0, 0), count, type_column, dest, tag, comm, ierr)
  end if
  !Reception in the last column
  if (rank == 1_8 ) then
    source = Int(0, 4)
    call mpi_recv(a(nb_columns - 1_8, 0), nb_lines, MPI_INTEGER8, source &
      , tag, comm, status, ierr)
  end if
  print *, 'I process ', rank, ', has a = ', a


  !Free the datatype
  call mpi_type_free(type_column, ierr)


  call mpi_finalize(ierr)

  end program prog_column
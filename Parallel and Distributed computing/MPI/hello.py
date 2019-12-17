from mpi4py import MPI

comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
p = comm.Get_size()

if my_rank != 0:
    message = f"hello from {my_rank}"
    comm.send(message, dest=0)
else:
    for proc_id in range(1, p):
        message = comm.recv(source=proc_id)
        print(f"Process 0 receives mmessafe grom process {proc_id} : {message}")

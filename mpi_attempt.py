import dpll
from mpi4py import MPI
import numpy as np

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    DPLL1 = dpll.DPLL(
        formula=dpll.extract_clauses(file='test.txt')[0],
        no_clauses=dpll.extract_clauses(file='test.txt')[2],
        no_variables=dpll.extract_clauses(file='test.txt')[1])
    vars_to_do = np.ndarray([x for x in range(DPLL1.no_variables, DPLL1.no_variables + 1)])
    # for i in range(0, size-1):
        # subgroup




    comm.Bcast(vars_to_do[0:size-1],my_var, root=0)
    if rank == 0:
        # for i in range(1, size):
            # comm.send(v/ars_to_do, dest=i)
        comm.Gather(, sendbuf, recvbuf)

    
    else:
        my_var = np.empty(1)
        comm.recv(my_var, source=0)
        DPLL.pure_literal_elim_with_index(my_var)
    # else:



if __name__ == "__main__":
    main()


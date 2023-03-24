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

    # for i in range(0, size-1):
        # subgroup


    if rank == 0:
        print ("=================START====================")
        vars_to_do = np.array([x for x in range(1, DPLL1.no_variables + 1)])
        print (vars_to_do)
        DPLL1.print_all()
        DPLL1.do_unit_prop_until_done()
        print ("=================UNIT PROP DONE====================")
        for i in range(1, size):
            comm.send(vars_to_do[i], dest=i)
    else:
        var = comm.recv(source=0)
        # DPLL1.pure_literal_elim_with_index(i=var)
        DPLL1.print_all()
        print ("=================LITERAL ELIM STARTING FOR {}====================".format(var))
        DPLL1.pure_literal_elim_with_index(i=var)
        DPLL1.print_all()
        print ("=================LITERAL ELIM DONE FOR {}====================".format(var))

    



if __name__ == "__main__":
    main()


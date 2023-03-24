import dpll
from mpi4py import MPI


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    DPLL1 = dpll.DPLL(
        formula=dpll.extract_clauses(file='test.txt')[0],
        no_clauses=dpll.extract_clauses(file='test.txt')[2],
        no_variables=dpll.extract_clauses(file='test.txt')[1])
    vars_to_do = [x for x in range(DPLL1.no_variables, DPLL1.no_variables + 1)]

    if rank == 0:
        
        pass
    # else:



if __name__ == "__main__":
    main()


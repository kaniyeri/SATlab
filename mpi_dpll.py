from mpi4py import MPI
import time

def extract_clauses(file):
    """Extract the clauses from the file. First line is the number of variables and number of clauses."""
    clauses = []
    with open(file) as f:
        for line in f:
            clause = line.split(',')
            clause = [int(x) for x in clause]
            clauses.append(clause)
        no_vars, no_clauses = clauses.pop(0)
        # print(clauses)
    return clauses, no_vars, no_clauses

class DPLL_Parallel:
    def __init__(self, clauses, no_variables, no_clauses):
        self.clauses = clauses
        self.assignments = {}
        self.no_variables = no_variables
        self.no_clauses = no_clauses

    def print_all(self):
        print(self.assignments)
        print(self.clauses)
        print(self.no_variables)
        print(self.no_clauses)

    def unit_propagation(self):
        unit_clauses = [clause for clause in self.clauses if len(clause) == 1]
        while True:
            if unit_clauses:
                for unit_clause in unit_clauses:
                    literal = unit_clause[0]
                    self.literal_unit_prop(literal)
                    unit_clauses.remove(unit_clause)
            else:
                return
            
    def literal_unit_prop(self, literal):
        self.assignments[literal] = True
        self.clauses.remove([literal])
        for clause in self.clauses:
            if clause.count(literal) > 0:
                self.clauses.remove(clause)
            elif clause.count(-literal) > 0:
                self.clauses.remove(clause)
                clause.remove(-literal)
                self.clauses.append(clause)
            else:
                continue

    def pure_literal_elimination_index(self, literal):
        prevEncountered = False
        if literal == 0:
            return 0
        for clause in self.clauses:
            if literal in clause:
                if -literal in clause:
                    continue
                else:
                    prevEncountered = True
            if -literal in clause:
                break
            if clause == self.clauses[-1] and prevEncountered:
                return 1
        return 0
    
    def pure_literal_elimination_propagation(self, literal):
        delete_clauses = []
        for clause in self.clauses:
            if clause.count(literal) > 0:
                delete_clauses.append(clause)
        for item in delete_clauses:
            self.clauses.remove(item)



def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    DPLL_Parallel1 = DPLL_Parallel(
        clauses=extract_clauses(file='test.txt')[0],
        no_variables=extract_clauses(file='test.txt')[1],
        no_clauses=extract_clauses(file='test.txt')[2]
    )

    if rank == 0:
        vars_to_do = [x for x in range(1, DPLL_Parallel1.no_variables + 1)]
        DPLL_Parallel1.unit_propagation()
        
        while(True):
            literal_elems = []
            for j in range(1, size):
                comm.send(1, dest=j)

            for i in range((DPLL_Parallel1.no_variables - 1) // (size - 1) + 1):
                for j in range(1, size):
                    if i*(size-1) + j - 1 < DPLL_Parallel1.no_variables:
                        comm.send(vars_to_do[i*(size-1) + j - 1], dest=j)   
                        literal_pure = comm.recv(source=j)
                        if literal_pure:
                            literal_elems.append(vars_to_do[i*(size-1) + j - 1])

            for elem in literal_elems:
                DPLL_Parallel1.assignments[elem] = True
                DPLL_Parallel1.pure_literal_elimination_propagation(elem)

            if len(DPLL_Parallel1.clauses) == 0:
                print("SAT")
                for j in range(1, size):
                    comm.send(0, dest=j)
                break
            if len(DPLL_Parallel1.clauses) == 1 and len(DPLL_Parallel1.clauses[0]) == 0:
                print("UNSAT")
                for j in range(1, size):
                    comm.send(0, dest=j)
                break
            
        print(DPLL_Parallel1.assignments)


    else:

        while(True):
            if comm.recv(source=0) == 0:
                break
            for i in range((DPLL_Parallel1.no_variables - 1) // (size - 1) + 1):
                if i*(size-1) + rank - 1 < DPLL_Parallel1.no_variables:
                    var = comm.recv(source=0)
                    literal_pure = DPLL_Parallel1.pure_literal_elimination_index(var)
                    comm.send(literal_pure, dest=0)



if __name__ == "__main__":
    main()
'''
5,3
1,-5,4,0
-1,5,3,4,0
-3,-4,0
This is the format for clauses.
'''
# import numba

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


class DPLL:
    def __init__(self, formula, no_variables, no_clauses):
        self.formula = formula
        self.assignments = {}
        self.clauses = []
        self.no_variables = no_variables
        self.no_clauses = no_clauses

        for clause in formula:
            self.clauses.append(list(set(clause)))

    def print_all(self):
        print(self.formula)
        print(self.assignments)
        print(self.clauses)
        print(self.no_variables)
        print(self.no_clauses)

    def unit_propogation(self):
        unit_clauses = [clause for clause in self.clauses if len(clause) == 1]
        if unit_clauses:
            for unit_clause in unit_clauses:
                literal = unit_clause[0]
                self.decide_up(literal)
        else:
            return
        # print(unit_clauses)
        pass

    def pure_literal_elim(self):
        for i in range(-self.no_variables, self.no_variables + 1):
            prevEncountered = False
            if i == 0:
                continue
            for clause in self.clauses:
                if i in clause:
                    if -i in clause:
                        self.clauses.remove(clause)
                    else:
                        prevEncountered = True
                if -i in clause:
                    break
                if clause == self.clauses[-1] and prevEncountered:
                    self.decide_ple(i)
                    # print("anmol"+str(i))
                    return
    def pure_literal_elim_with_index(self,i):
            prevEncountered = False
            if i == 0:
                return
            for clause in self.clauses:
                if i in clause:
                    if -i in clause:
                        self.clauses.remove(clause)
                    else:
                        prevEncountered = True
                if -i in clause:
                    break
                if clause == self.clauses[-1] and prevEncountered:
                    self.decide_ple(i)
                    print("anmol"+str(i))
                    return

    def decide_up(self, literal):
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

    def decide_ple(self, literal):
        self.assignments[literal] = True
        delete_clause = []
        for clause in self.clauses:
            if clause.count(literal) > 0:
                delete_clause.append(clause)
        for item in delete_clause:
            self.clauses.remove(item)

    def solve(self):
        while True:
            self.unit_propogation()
            self.pure_literal_elim()
            if len(self.clauses) == 0:
                print("SAT")
                return
            if len(self.clauses) == 1 and len(self.clauses[0]) == 0:
                print("UNSAT")
                return
        # self.unit_propogation()
        # self.pure_literal_elim()
    def do_unit_prop_until_done(self):
        unit_clauses = [clause for clause in self.clauses if len(clause) == 1]
        while True:
            if unit_clauses:
                for unit_clause in unit_clauses:
                    literal = unit_clause[0]
                    self.decide_up(literal)
                    unit_clauses.remove(unit_clause)
            else:
                return
                        


def main():
    # extract_clauses(file='test.txt')
    DPLL1 = DPLL(
        formula=extract_clauses(file='test.txt')[0],
        no_clauses=extract_clauses(file='test.txt')[2],
        no_variables=extract_clauses(file='test.txt')[1])

    # measure time taken for DPLL.solve()
    t1 = time.perf_counter()
    DPLL1.solve()
    t2 = time.perf_counter()
    print(f"Time taken for DPLL.solve(): {t2 - t1:0.4f} seconds")
    DPLL1.print_all()


if __name__ == '__main__':
    main()

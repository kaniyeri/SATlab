'''
5,3
1,-5,4,0
-1,5,3,4,0
-3,-4,0
This is the format for clauses.
'''


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
        # if unit_clauses:
        #     unit_clause = unit_clauses[0]
        #     literal = unit_clause[0]
        print(unit_clauses)
        pass
    def solve(self):
        

def main():
    # extract_clauses(file='test.txt')
    DPLL1 = DPLL(formula=extract_clauses(file='test.txt')[0],no_clauses=extract_clauses(file='test.txt')[2],no_variables=extract_clauses(file='test.txt')[1])
    DPLL1.print_all()
    DPLL1.unit_propogation()



if __name__ == '__main__':
    main()

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
    def __init__(self, formula, no_vars, no_clauses):
        self.formula = formula
        self.no_vars = no_vars
        self.no_clauses = no_clauses
        self.assignments = {}
        self.unassigned = []
        self.clauses = []

        for clause in formula:
            self.clauses.append(clause)

        for i in range(1,self.no_vars+1):
            for clause in self.clauses:
                if (i in clause) or (-i in clause):
                    self.unassigned.append(i)
                    self.unassigned.append(-i)
                    break

    def unit_literal(self):
        for clause in self.clauses:
            if(len(clause) == 1):
                return clause[0]
        return None
    
    def unit_prop(self, literal):
        self.assignments[literal] = True
        self.unassigned.remove(literal)
        self.unassigned.remove(-literal)

        self.clauses.remove([literal])

        for clause in self.clauses:
            if(clause.count(literal) > 0):
                self.clauses.remove(clause)
            elif(clause.count(-literal) > 0):
                self.clauses.remove(clause)
                clause.remove(-literal)
                self.clauses.append(clause)

    def pure_literal(self):
        for literal in self.unassigned:
            prevEncountered = False

            for clause in self.clauses:
                if literal in clause:
                    if -literal in clause:
                        continue
                    else:
                        prevEncountered = True
                elif -literal in clause:
                    break

                if (clause == self.clauses[-1]) and prevEncountered:
                    return literal
        return None
    
    def pure_prop(self, literal):
        self.assignments[literal] = True
        self.unassigned.remove(literal)
        for clause in self.clauses:
            if -literal in clause:
                self.unassigned.remove(-literal)
                break
        for clause in self.clauses:
            if literal in clause:
                self.clauses.remove(clause)
            
    def DPLL_and_literal(self, literal):
        new_clauses = []
        for clause in self.clauses:
            if literal in clause:
                continue
            elif -literal in clause:
                temp = clause.copy()
                temp.remove(-literal)
                new_clauses.append(temp)
                del temp
            else:
                new_clauses.append(clause)
        
        return DPLL(formula=new_clauses, no_clauses=len(new_clauses), no_vars=self.no_vars)

    def add_assignments(self, new_assignments, literal):
        self.assignments[literal] = True
        self.unassigned.remove(literal)
        self.unassigned.remove(-literal)

        for assign in new_assignments:
            self.assignments[assign] = True
            self.unassigned.remove(assign)
            self.unassigned.remove(-assign)

            for clause in self.clauses:
                if assign in clause:
                    self.clauses.remove(clause)
                elif -assign in clause:
                    self.clauses.remove(clause)
                    clause.remove(-assign)
                    self.clauses.append(clause)

    def DPLL_procedure(self):
        unit_literal = self.unit_literal()
        # print('unit', unit_literal)
        while(unit_literal):
            self.unit_prop(unit_literal)
            unit_literal = self.unit_literal()
            # print('unit', unit_literal)
        self.print()

        pure_literal = self.pure_literal()
        # print('pure', pure_literal)
        while(pure_literal):
            self.pure_prop(pure_literal)
            pure_literal = self.pure_literal()
            # print('pure', pure_literal)
        self.print()

        if len(self.clauses) == 0:
            return True
        elif [] in self.clauses:
            return False
        
        literal = self.unassigned[0]
        print(literal)
        DPLL_and_literal = self.DPLL_and_literal(literal)
        DPLL_and_not_literal = self.DPLL_and_literal(-literal)

        andresult = DPLL_and_literal.DPLL_procedure()
        andnotresult = DPLL_and_not_literal.DPLL_procedure()
        if andresult:
            self.add_assignments(list(DPLL_and_literal.assignments.keys()), literal)
        elif andnotresult:
            self.add_assignments(list(DPLL_and_not_literal.assignments.keys()), -literal)
        return andresult or andnotresult

    def print(self):
        print('clauses', self.clauses)
        print('assignments', self.assignments)
        print('unassigned', self.unassigned)
        print('---------------------------------------------------')


formula, no_vars, no_clauses = extract_clauses('../test3.txt')
dpll1 = DPLL(formula=formula, no_vars=no_vars, no_clauses=no_clauses)
dpll1.print()
print(dpll1.DPLL_procedure())
def extract_clauses(file):
    """Extract the clauses from the file. First line is the number of variables and number of clauses."""
    clauses = []
    with open(file) as f:
        for line in f:
            clause = line.split()
            if 'p' in clause:
                no_vars, no_clauses = int(clause[2]), int(clause[3])
                continue
            clause = [int(x) for x in clause[:-1]]
            clauses.append(clause)
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
        clauses = self.clauses.copy()
        for clause in clauses:
            if(clause.count(literal) > 0):
                self.clauses.remove(clause)
            elif(clause.count(-literal) > 0):
                self.clauses.remove(clause)
                clause.remove(-literal)
                self.clauses.append(clause)
        del clauses

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
        self.unassigned.remove(-literal)

        clasues = self.clauses.copy()
        for clause in clasues:
            if literal in clause:
                self.clauses.remove(clause)
        del clasues
            
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
        for assign in new_assignments:
            self.assignments[assign] = True
            self.unassigned.remove(assign)
            self.unassigned.remove(-assign)

            clauses = self.clauses.copy()
            for clause in clauses:
                if assign in clause:
                    self.clauses.remove(clause)
                elif -assign in clause:
                    self.clauses.remove(clause)
                    clause.remove(-assign)
                    self.clauses.append(clause)
            del clauses

    def DPLL_procedure(self):
        unit_literal = self.unit_literal()
        while(unit_literal):
            self.unit_prop(unit_literal)
            unit_literal = self.unit_literal()

        pure_literal = self.pure_literal()
        while(pure_literal):
            self.pure_prop(pure_literal)
            pure_literal = self.pure_literal()

        if len(self.clauses) == 0:
            return True
        elif [] in self.clauses:
            return False
        
        literal = self.unassigned[0]
        clauses = self.clauses.copy()
        clauses.append([literal])
        DPLL_and_literal = DPLL(formula=clauses, no_clauses=self.no_clauses, no_vars=self.no_vars)
        clauses.remove([literal])
        clauses.append([-literal])
        DPLL_and_not_literal = DPLL(formula=clauses, no_clauses=self.no_clauses, no_vars=self.no_vars)
        del clauses 

        andresult = bool(DPLL_and_literal.DPLL_procedure())
        if andresult:
            self.add_assignments(list(DPLL_and_literal.assignments.keys()), literal)
        
        andnotresult = bool(DPLL_and_not_literal.DPLL_procedure())
        if (andnotresult and (not andresult)):
            self.add_assignments(list(DPLL_and_not_literal.assignments.keys()), -literal)
        return (andresult or andnotresult)

    def print(self):
        print('clauses', self.clauses)
        print('assignments', self.assignments)
        print('---------------------------------------------------')


formula, no_vars, no_clauses = extract_clauses('/home/nx6xe23/github-repos/SATlab/test3.txt')
dpll1 = DPLL(formula=formula, no_vars=no_vars, no_clauses=no_clauses)
print(dpll1.DPLL_procedure())
assignments = list(dpll1.assignments.keys())
sat_solved = []
for i in range(1, no_vars+1):
    if i in assignments:
        sat_solved.append(i)
    elif -i in assignments:
        sat_solved.append(-i)

print(sat_solved)
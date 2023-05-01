import random
from mpi4py import MPI

class DPLL:
    def __init__(self, n_vars, n_clauses):
        self.n_vars = n_vars
        self.n_clauses = n_clauses
        self.clauses = []
        self.assignments = []
        self.contradiction = False

    def add_clause(self, clause):
        self.clauses.append(clause)
    
    def is_empty(self):
        return True if (len(self.clauses) == 0) else False
    
    def has_contradiction(self):
        return self.contradiction
    

def cnf_formula(filename):
    for line in open(filename):
        if line.startswith('p'):
            n_vars, n_clauses = line.split()[2:4]
            formula = DPLL(n_vars=int(n_vars), n_clauses=int(n_clauses))
            continue
        clause = [int(x) for x in line[:-2].split()]
        formula.add_clause(clause)
    return formula 


def bool_const_prop(formula, literal):
    new_formula = DPLL(formula.n_vars, formula.n_clauses)
    new_formula.assignments = formula.assignments.copy()
    for clause in formula.clauses:
        if literal in clause: continue
        if -literal in clause:
            new_clause = [x for x in clause if x != -literal]
            if len(new_clause) == 0:
                new_formula.contradiction = True
                return new_formula
            new_formula.add_clause(new_clause)
            
        else:
            new_formula.add_clause(clause)
    del formula
    return new_formula

def unit_prop(formula):
    unit_clauses = [c for c in formula.clauses if len(c) == 1]
    while(len(unit_clauses) > 0):
        unit = unit_clauses[0]
        formula = bool_const_prop(formula, unit[0])
        formula.assignments.append(unit[0])
        unit_clauses = [c for c in formula.clauses if len(c) == 1]
        if formula.has_contradiction():
            return formula
        if len(formula.clauses) == 0:
            return formula
    return formula

def choose_literal(formula):
    clause = random.choice(formula.clauses)
    return random.choice(clause)

def backtracking(formula):
    formula = unit_prop(formula)

    if formula.has_contradiction():
        return None
    if formula.is_empty():
        return formula.assignments
    
    variable = choose_literal(formula)
    new_formula = bool_const_prop(formula, variable)
    new_formula.assignments.append(variable)
    solution = backtracking(new_formula)

    if not solution:
        new_formula = bool_const_prop(formula, -variable)
        new_formula.assignments.append(-variable)
        solution = backtracking(new_formula)
    return solution


formula = cnf_formula('test3.txt')
solution = backtracking(formula)
print(solution)
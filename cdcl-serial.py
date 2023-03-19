from collections import deque

class CDCL:
    def __init__(self, formula, no_variables, no_clauses):
        self.formula = formula
        self.assignments = {}
        self.clauses = []
        self.no_variables = no_variables
        self.no_clauses = no_clauses
        self.queue = deque()

        for clause in formula:
            self.clauses.append(list(set(clause)))

    def unit_propogation(self):
        unit_clauses  =[clause for clause in self.clauses if len(clause) == 1]
        if len(unit_clauses):
            unit_clause = unit_clauses[0]
            literal = unit_clause[0]
            self.decide(literal)
        else:
            return
        
    def decide(self, literal):
        self.assignments[literal] = True
        self.queue.append(literal)



class CDCL:
    def __init__(self, formula):
        self.formula = formula
        self.assignments = {}
        self.clauses = []

        for clause in formula:
            self.clauses.append(set(clause))

    def unit_propogation(self):
        unit_clauses  =[clause for clause in self.clauses if len(clause) == 1]
        if not unit_clauses:
            break
        unit_clause = unit_clauses[0]
        literal = unit_clause[0]
        self.decide(literal)

    def decide(self, literal):
        self.assignments[literal] = True
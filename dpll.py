'''
1,-5,4,0
-1,5,3,4,0
-3,-4,0
This is the format for clauses.
'''
def extract_clauses(file):
    """Extract the clauses from the file."""
    clauses = []
    with open(file) as f:
        for line in f:
            clause = line.split(',')
            clause = [int(x) for x in clause]
            clauses.append(clause)
    return clauses

def unit_propagate(clauses, unit):
    """Propagate the unit clause and remove it from the list of clauses."""

def main():
    print(extract_clauses('sat.txt'))


if __name__ == '__main__':
    main()
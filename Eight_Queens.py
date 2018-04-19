import numpy as np
import itertools as itt

def queens(num_queens):
    diag = np.diag(np.ones(num_queens))
    pass

diag = np.diag(np.ones(4, dtype='int'))
diag = diag.tolist()
test = itt.permutations(diag)

combos = [subset for subset in test]
print(combos)

#TODO use trace(matrix) to determine if queens are diagonal
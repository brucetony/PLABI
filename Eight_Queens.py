import numpy as np
import itertools as itt

def queens(num_queens):
    diag = np.diag(np.ones(num_queens, dtype='int'))
    diag_list = diag.tolist()
    combos = [subset for subset in itt.permutations(diag_list)]
    pass

diag = np.diag(np.ones(4, dtype='int'))
test = itt.permutations(diag)

combos = [subset for subset in test]
print(type(diag))
print(type(combos[0]))

#TODO use trace(matrix) to determine if queens are diagonal
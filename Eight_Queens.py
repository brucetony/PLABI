import numpy as np
import itertools as itt
import string

def chess_positions(binary_list):
    positions = []
    letters = string.ascii_lowercase
    letter_dict = dict(zip(range(len(letters)), letters))
    for i in range(len(binary_list)):
        for j in range(len(binary_list[i])):
            if binary_list[i][j] != 0:
                position = letter_dict[j] + str(i+1)
                positions.append(position)
    return positions


def queens(num_queens, all_solns = False):
    #Generate game board with queens using diagonal matrix
    diag = np.diag(np.ones(num_queens, dtype='int'))

    #Create all possible board configurations where no 2 queens are in the same row or column
    matrices = []
    for permuation in itt.permutations(diag):
        output = np.concatenate([array for array in permuation], axis=0)
        matrices.append(output.reshape((num_queens, num_queens)))

    #Create empty list of valid game boards
    valid_setups = []

    #While loop through all matrices and discard invalid ones (2+ queens on diagonal)
    counter = 0
    M = len(matrices[0])
    while counter < len(matrices):
        print(counter)
        trace_values = []
        trace_values.append(np.trace(matrices[counter]))
        trace_values.append(np.trace(np.rot90(matrices[counter])))
        if trace_values[0] > 1 or trace_values[1] > 1:
            counter += 1
            continue

        current_matrix = matrices[counter]

        #Top left matrix
        i = M - 1
        while i > 1:
            trace_values.append(np.trace(np.rot90(current_matrix[0:i, 0:i])))
            i -= 1

        #Bottom left matrix
        i = 1
        j = M-1
        while j > 1:
            trace_values.append(np.trace(current_matrix[i:M, 0:j]))
            i += 1
            j -= 1

        #Top right matrix
        i = M - 1
        j = 1
        while i > 1:
            trace_values.append(np.trace(current_matrix[0:i, j:]))
            i -= 1
            j += 1

        #Bottom right matrix
        i = 1
        while i < M:
            trace_values.append(np.trace(np.rot90(current_matrix[i:, i:])))
            i += 1

        if max(trace_values) <= 1:
            valid_setups.append(current_matrix)

        counter += 1

        if all_solns is False:
            if len(valid_setups) > 0:
                break

    positions_lists = []
    for array in valid_setups:
        array_list = array.tolist()
        positions_lists.append(chess_positions(array_list))

    return positions_lists

print(queens(8))
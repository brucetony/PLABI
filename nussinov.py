import numpy as np


def delta(i, j, sequence):
    """
    Helper function to determine if new match is made
    :param i: Current 1st position in sequence
    :param j: Current 2nd position in sequence
    :param sequence: RNA sequence being interrogated
    :return: 1 if match made, 0 if no match
    """
    comp_pairs = [('A', 'U'), ('C', 'G'), ('G', 'C'), ('U', 'A')]
    listed_seq = list(sequence)

    # Determine delta(i, j) i.e. whether positions i and j form a base pair
    if (listed_seq[i], listed_seq[j]) in comp_pairs:
        return 1
    else:
        return 0


def subseq_score(i, j, sequence, h_loop=1):
    """
    Generate a score using recursion for use in a dynamic programming matrix
    :param i: Current ith position in the sequence
    :param j: Current jth position in the sequence
    :param sequence: Sequence being interrogated
    :param h_loop: (Opt) Adjust the minimum subsequence length
    :return:
    """
    if j-i+1 < h_loop+2:  # If subseq is too small return 0
        return 0
    else:
        # For cases 1 and 2 we need the unpaired score
        unpaired = subseq_score(i+1, j-1, sequence, h_loop=h_loop) + delta(i, j, sequence)

        # For cases 3 and 4 we find the max score of paired values (check to see if they are paired)
        paired = [subseq_score(i, k, sequence, h_loop=h_loop)
                  + subseq_score(k+1, j, sequence, h_loop=h_loop) for k in range(i, j)
                  if delta(k+1, j, sequence) == 1 and delta(i, k, sequence) == 1]

        # In case the paired comprehension returns nothing
        if not paired:
            paired = [0]

    return max(unpaired, max(paired))


def backtrack(i, j, sequence, completed_pair_matrix, matched_positions, h_loop=1):
    """
    Determiens proper base pairing based on a completed dynamic scoring matrix created by subseq_score
    :param i: Current ith position in the sequence, initialize to 0
    :param j: Current jth position in the sequence, initialize to len(sequence)-1
    :param sequence: RNA sequence being interrogated
    :param completed_pair_matrix: Completed dynamic scoring matrix generated by subseq_score()
    :param matched_positions: List containing the optimal matched positions for the seq, initialize with empty list []
    :param h_loop: The minimum acceptable length of the loop within the RNA structure
    :return: List of indices of optimal base pairings within the given sequence
    """

    # Requirement: the sequence length must be greater than h_loop + 1 to continue
    if j-i+1 >= h_loop+2:
        if completed_pair_matrix[i][j] == completed_pair_matrix[i+1][j-1] + delta(i, j, sequence):
            # If new match made then append to list
            if delta(i, j, sequence) == 1:  # If 0 then no match so we can skip, only care about 1
                matched_positions.append((i, j))
            backtrack(i+1, j-1, sequence, completed_pair_matrix, matched_positions, h_loop=h_loop)
        else:
            # Find k in range (i,j) and get list of paired of comp bases
            for k in range(i, j-1):
                if completed_pair_matrix[i][j] == completed_pair_matrix[i][k] + completed_pair_matrix[k+1][j]:
                    backtrack(i, k, sequence, completed_pair_matrix, matched_positions, h_loop=h_loop)
                    backtrack(k+1, j, sequence, completed_pair_matrix, matched_positions, h_loop=h_loop)

                    # Once we have found that k value we break from the loop
                    break

    return matched_positions


def display_pairing(sequence, optimal_pair_list):
    """
    Shows the pairing within an RNA seq using '(' and ')'
    :param sequence: RNA sequence being interrogated
    :param optimal_pair_list: Optimal (longest) list of base pairs within the sequence as determined by backtrack()
    :return: Graphical string showing matching base pairs within the chosen sequence
    """
    pair_display = ['.'] * len(sequence)  # Generate list of '.' to be replaced
    for pair in optimal_pair_list:
        pair_display[pair[0]] = '('
        pair_display[pair[1]] = ')'
    return ''.join(pair_display)


def nussinov(sequence, h_loop=1):
    # Initialize dynamic programming matrix
    N = len(sequence)
    pair_matrix = np.zeros((N, N), dtype='int')
    
    # Generate scores for dynamic matrix using subseq score function
    for i in range(N):
        for j in range(i, N):
            pair_matrix[i][j] = subseq_score(i, j, sequence, h_loop=h_loop)
            pair_matrix[j][i] = pair_matrix[i][j]  # Make matrix reflective

    # Find optimal pairing solution
    optimal_base_pairing = backtrack(0, N-1, sequence, pair_matrix, h_loop=h_loop, matched_positions=[])

    # print('Backtracking completed\nNumber of possible solutions:', optimal_solutions(pair_list),
    #       '\nDisplaying first solution\n')

    # optimal_base_pairing.sort(key=len, reverse=True)
    print('\nOptimal matched base pairing positions in RNA sequence:\n{}\n'.format(optimal_base_pairing))
    print(sequence)
    print(display_pairing(sequence, optimal_base_pairing))
    print('\nNumber of base pairs found:', len(optimal_base_pairing))
    return pair_matrix


# For testing
seq = 'AUCGGAGCAUUUUUUGCUCCGACGCAGCCUCAUGCUUUUUU'
dp = nussinov(seq, h_loop=1)

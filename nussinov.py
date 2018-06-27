import numpy as np

def subseq_score(i, j, sequence, min_seq_length=3):
    comp_pairs = [('A', 'U'), ('C', 'G'), ('G', 'C'), ('U', 'A')]
    listed_seq = list(sequence)

    # Determine delta(i, j) i.e. whether positions i and j form a base pair
    if (listed_seq[i], listed_seq[j]) in comp_pairs:
        delta = 1
    else:
        delta = 0

    if j-i+1 < min_seq_length:  # If subseq is too small return 0
        return 0
    else:
        # For cases 1 and 2 we need the unpaired score
        unpaired = subseq_score(i+1, j-1, sequence, min_seq_length=min_seq_length) + delta

        # For cases 3 and 4 we find the max score of paired values (check to see if they are paired)
        paired = [subseq_score(i, k, sequence, min_seq_length=min_seq_length)
                  + subseq_score(k+1, j, sequence, min_seq_length=min_seq_length) for k in range(i, j)
                  if (listed_seq[k], listed_seq[j]) in comp_pairs]

        # In case the paired comprehension returns nothing
        if not paired:
            paired = [0]

    return max(unpaired, max(paired))


def backtrack(sequence, pairing_matrix):
    


def nussinov(sequence):
    # Initialize dynamic programming matrix
    N = len(sequence)
    pair_matrix = np.zeros((N, N), dtype='int')
    
    # Generate scores for dyanmic matrix using subseq score function
    for i in range(N):
        for j in range(i, N):
            pair_matrix[i][j] = subseq_score(i, j, sequence, min_seq_length=3)
            pair_matrix[j][i] = pair_matrix[i][j]  # Make matrix reflective
    


    return pair_matrix



seq = 'AUCGGAGCAUUUUUUGCUCCGACGCAGCCUCAUGCUUUUUU'
# seq = 'AUCGGAGCAUUUUUUGCUCCGA'
print(nussinov(seq))
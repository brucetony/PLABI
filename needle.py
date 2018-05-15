import pandas as pd
import numpy as np


def read_score_matrix(input_matrix):
    '''
    Converts a blosum matrix into a usable (pandas) format
    :param input_matrix: Txt file containing score matrix with values separated by "  "
    :return: Pandas dataframe
    '''
    with open(input_matrix, 'r') as file:
        string_lines = file.read().splitlines()

    reduced_lines = []
    for string in string_lines:
        string_list = string.split(' ')  # Remove double spaces
        reduced_lines.append(string_list)
    reduced_lines = [list(filter(None, strings)) for strings in reduced_lines]  # Remove empty lists
    aa_list = reduced_lines[0]
    sliced_scores = [score[1:] for score in reduced_lines[1:] if score]
    df = pd.DataFrame(sliced_scores, columns=aa_list, index=aa_list)
    df[aa_list] = df[aa_list].astype(int)
    return df


def alignment_builder(seqA, seqB, trace_matrix):
    pass


def needleman_wunsch_global(seqA, seqB, score_matrix_file, gap_penalty=-8):
    M = len(seqA)+1  # Extra space for gap at beginning
    N = len(seqB)+1  # Extra space for gap at beginning
    scoring_matrix = read_score_matrix(score_matrix_file)
    w = gap_penalty

    # Create data matrics
    align_matrix = np.zeros((M, N), dtype=int)
    trace_matrix = np.empty((M, N), dtype=str)

    # Initialize matrices
    for j in range(N):
        align_matrix[0][j] = w*j
    for i in range(M):
        align_matrix[i][0] = w*i

    for i in range(1, M):
        for j in range(1, N):
            aa_A = list(seqA)[i-1]  # Get amino acid at index i for seqA
            aa_B = list(seqB)[j-1]  # Get amino acid at index j for seqB

            # Define movement directions
            diag = align_matrix[i-1][j-1] + scoring_matrix.at[(aa_A, aa_B)]
            vertical = align_matrix[i-1][j] + w
            horizonal = align_matrix[i][j-1] + w

            max_scorer = max(diag, vertical, horizonal)  # Get max score
            align_matrix[i][j] = max_scorer

            #
            if max_scorer == diag:
                trace_matrix[i][j] = 'D'
            elif max_scorer == vertical:
                trace_matrix[i][j] = 'V'
            else:
                trace_matrix[i][j] = 'H'

    # Organize into data frames for output
    col_list = [' '] + list(seqB)
    index_list = [' '] + list(seqA)
    align_df = pd.DataFrame(align_matrix, columns=col_list, index=index_list)

    return align_df


score_matrix = read_score_matrix('blosum62.txt')

seqs1 = ["THRQATWQPPLERMANGRQVE", "RAYMQNDLVKVRYYACHT"]
seqs = ["PAWHEAE", "HEAGAWGHEE"]

print(needleman_wunsch_global(seqs[0], seqs[1], 'blosum62.txt'))

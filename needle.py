import os
import pandas as pd
import numpy as np
import sys

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


def alignment_builder(columns, rows, trace_matrix):

    # Instantiate alignment lists
    align_a = []
    align_b = []

    i = len(rows)-1
    j = len(columns)-1

    while trace_matrix[i][j] != 'S':
        if trace_matrix[i][j] == 'D':
            align_a.append(rows[i])
            align_b.append(columns[j])
            i -= 1
            j -= 1
        elif trace_matrix[i][j] == 'V':
            align_a.append(rows[i])
            align_b.append("-")
            i -= 1
        elif trace_matrix[i][j] == 'H':
            align_a.append("-")
            align_b.append(columns[j])
            j -= 1

    # Reverse sequence and join string
    alignments = [''.join(align_a[::-1]), ''.join(align_b[::-1])]

    return alignments


def needleman_wunsch_global(seqA, seqB, score_matrix_file, gap_penalty, show_alignment=False):
    M = len(seqA)+1  # Extra space for gap at beginning
    N = len(seqB)+1  # Extra space for gap at beginning
    scoring_matrix = read_score_matrix(score_matrix_file)
    w = gap_penalty

    # Create data matrics
    align_matrix = np.zeros((M, N), dtype=int)
    trace_matrix = np.empty((M, N), dtype=str)

    # Initialize matrices
    for i in range(M):
        align_matrix[i][0] = w*i
        trace_matrix[i][0] = 'V'
    for j in range(N):
        align_matrix[0][j] = w*j
        trace_matrix[0][j] = 'H'
    trace_matrix[0][0] = 'S'  # S for STOP


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

            # Fill trace_matrix with directions
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

    if show_alignment:
        print(align_df)

    # Create alignment and symbols for matching - '|' = match, ':' = positive score
    opt_align = alignment_builder(col_list, index_list, trace_matrix)
    opt_seq1 = list(opt_align[0])
    opt_seq2 = list(opt_align[1])

    symbol_list = [' '] * len(opt_align[0])
    for i, symbol in enumerate(symbol_list):
        if opt_seq1[i] == '-' or opt_seq2[i] == '-':
            continue
        elif opt_seq1[i] == opt_seq2[i]:
            symbol_list[i] = '|'
        elif scoring_matrix.at[(opt_seq1[i], opt_seq2[i])] > 0:
            symbol_list[i] = ':'

    # Print optimal alignments/symbols
    print('Alignment score: {}\n'.format(align_matrix[M-1][N-1]))
    print('{}\n{}\n{}'.format(opt_align[0], ''.join(symbol_list), opt_align[1]))

    return opt_align


def fasta_parser(fasta_file):
    assert os.path.splitext(fasta_file)[1] == '.fasta'
    with open(fasta_file, 'r') as file:
        sequence_lines = file.read().splitlines()[1:]
    return ''.join(sequence_lines)


# For testing
# seqs = ["THRQATWQPPLERMANGRQVE", "RAYMQNDLVKVRYYACHT"]
# first_seq = fasta_parser("RNAS1_minke-whale.fasta")
# second_seq = fasta_parser("RNAS1_red-kangaroo.fasta")
# #needleman_wunsch_global(seqs[0], seqs[1], 'blosum62.txt', -8)
# needleman_wunsch_global(first_seq, second_seq, 'blosum62.txt', -8)


# For running in cmd line
first_seq = fasta_parser(sys.argv[3])
second_seq = fasta_parser(sys.argv[4])

needleman_wunsch_global(first_seq, second_seq, sys.argv[2], int(sys.argv[1]))
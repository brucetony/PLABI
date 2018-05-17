import os
import pandas as pd
import numpy as np
import sys

def read_score_matrix(input_matrix):
    '''
    Converts a blosum matrix into a usable (pandas) format
    :param input_matrix: Txt file containing score matrix with values separated by "  "
    :return: Pandas dataframe containing scoring matrix information
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


def affine_gaps(i_pos, j_pos, trace_matrix, direction, d=-8, e=-2):
    '''
    Helper function to generate a penalty score for alignment scoring. Utilizes gap extension penalty added to a\
    initial gap penalty
    :param i_pos: Current row position in alignment matrix
    :param j_pos: Current column position in alignment matrix
    :param trace_matrix: Matrix containing directions for building alignments
    :param direction: Current direction being checked (either 'V' or 'H')
    :param d: initial gap penalty (w)
    :param e: gap extension penalty
    :return: penalty score
    '''
    gap_length = 1  # Length of gap sequence, start at 1 since gap must at least 1 long to exist
    i = i_pos
    j = j_pos
    if direction == 'V':
        while i >= 0 and trace_matrix[i-1][j] == 'V':
            gap_length += 1
            i -= 1
    if direction == 'H':
        while j >= 0 and trace_matrix[i][j-1] == 'H':
            gap_length += 1
            j -= 1
    return d+e*(gap_length-1)  # Initial gap penalty multiplied by e times length - 1


def alignment_builder(columns, rows, trace_matrix, align_matrix, align='global'):
    '''
    Creates the aligned sequences using the trace_matrix directions
    :param columns: Sequence 2 to be used as a reference for building
    :param rows: Sequence 1 to be used as a reference for building
    :param trace_matrix: Matrix containing direction ('V', 'H', 'D', and 'S') which dictates whether a residue or gap\
    is added to aligned sequence
    :param align_matrix: Pandas scoring matrix used to determine where to start the alignment
    :param align: 'global' starts alignment at end of two sequences , 'local' starts at max score in align_matrix
    :return: List with the two "aligned" sequences
    '''
    # Instantiate alignment lists
    align_a = []
    align_b = []

    if align == 'global':
        i = len(rows)-1
        j = len(columns)-1
    elif align == 'local':
        row_maxs = list(align_matrix.max(axis=1))
        col_maxs = list(align_matrix.max(axis=0))
        i = row_maxs.index(max(row_maxs))
        j = col_maxs.index(max(col_maxs))

    while trace_matrix[i][j] != 'S':
        if align_matrix.iloc[i, j] == 0 and align == 'local':  # Break if a score of 0 is reached in local alignment
            break
        elif trace_matrix[i][j] == 'D':
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


def sequence_alignment(seqA, seqB, score_matrix_file, gap_penalty, align_type='global',\
                       affine=False, ext_penalty=-2, show_alignment=False):
    '''
    Uses either global (Needleman-Wunsch) or local (Smith-Waterman) alignment algorithms based on what the \
    user choose for align_type. Print out a graphical representation of the alignment using a "|" for a \
    matched set of residues and a ":" for a conservative (positive score) substitution. It will also print\
    the alignment score as well as the sequence identity (perfectly matched residues divided by all aligned residues)\
    and the sequence similarity (similar residues divided by all aligned residues). The graphical output includes \
    the residue number at the end of the segment.
    :param seqA: Sequenced to be aligned provided as a string or .fasta file
    :param seqB: Sequenced to be aligned provided as a string or .fasta file
    :param score_matrix_file: Pre-made matrix containing scores for matched residues
    :param gap_penalty: Penalty given to score for mis-matched residues. Default set to -8
    :param align_type: Either 'global' or 'local'
    :param show_alignment: Boolean, if True, will also print the score matrix for the two sequences
    :param e: Integer (usually negative), defines the gap extension penalty
    :param affine: Boolean which decides whether to use smaller gap penalty for each gap used after the first
    :return: A list with the two optimally aligned sequences including their gaps
    '''
    if affine:  # To make sure one does not use affine gaps with local
        assert align_type == 'global'
    
    M = len(seqA)+1  # Extra space for gap at beginning
    N = len(seqB)+1  # Extra space for gap at beginning
    scoring_matrix = read_score_matrix(score_matrix_file)
    w = gap_penalty

    # Create data matrics align = scoring, trace = directions for building sequence after
    align_matrix = np.zeros((M, N), dtype=int)
    trace_matrix = np.empty((M, N), dtype=str)

    # Initialize matrices
    for i in range(M):
        if align_type == 'global':  # If global then first row/column has decay
            if affine:
                align_matrix[i][0] = w + ext_penalty*(i-1)
            else:
                align_matrix[i][0] = w*i
        elif align_type == 'local':  # If local then first row/column set to 0
            align_matrix[i][0] = 0
        trace_matrix[i][0] = 'V'
    for j in range(N):
        if align_type == 'global':
            if affine:
                align_matrix[0][j] = w + ext_penalty*(j-1)
            else:
                align_matrix[0][j] = w*j
        elif align_type == 'local':
            align_matrix[0][j] = 0
        trace_matrix[0][j] = 'H'
    align_matrix[0][0] = 0
    trace_matrix[0][0] = 'S'  # S for STOP


    for i in range(1, M):
        for j in range(1, N):
            aa_A = list(seqA)[i-1]  # Get amino acid at index i for seqA
            aa_B = list(seqB)[j-1]  # Get amino acid at index j for seqB

            # Define movement directions
            diag = align_matrix[i-1][j-1] + scoring_matrix.at[(aa_A, aa_B)]  # .at[] works because cols/rows are sets
            if affine:
                vertical = align_matrix[i-1][j] + affine_gaps(i, j, trace_matrix, 'V', d=w, e=ext_penalty)
                horizontal = align_matrix[i][j-1] + affine_gaps(i, j, trace_matrix, 'H', d=w, e=ext_penalty)
            else:
                vertical = align_matrix[i-1][j] + w
                horizontal = align_matrix[i][j-1] + w

            if align_type == 'global':
                max_scorer = max(diag, vertical, horizontal)  # Get max score for global alignment
            elif align_type == 'local':
                max_scorer = max(diag, vertical, horizontal, 0)
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
    opt_align = alignment_builder(col_list, index_list, trace_matrix, align_df, align=align_type)
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

    # Calculate sequence similarity and sequence identity
    similarity = round(100*(symbol_list.count('|')+symbol_list.count(':'))/len(opt_seq1), 2)
    identity = round(100*symbol_list.count('|')/len(opt_seq1), 2)

    # Divide the seqs and symbols into lengths of 50 for visibility
    i = 0
    chunk_size = 100
    opt1_chunk = []
    opt2_chunk = []
    symbol_chunk = []
    while i < len(opt_seq1):
        opt1_chunk.append(''.join(opt_seq1[i:i+chunk_size]))
        opt2_chunk.append(''.join(opt_seq2[i:i+chunk_size]))
        symbol_chunk.append(''.join(symbol_list[i:i+chunk_size]))
        i += chunk_size

    # Print score -> optimal alignments/symbols -> Seq similarity/identity percentages
    print('Alignment score: {}\n'.format(align_matrix[M-1][N-1]))
    seq_length = 0  # To track length of aligned sequence displayed
    for i in range(len(opt1_chunk)):
        # Add nucleotide counter to help after symbol output
        seq_length += len(symbol_chunk[i])  # Add length of aligned seq to counter
        print('{}\n{}  {}\n{}\n'.format(opt1_chunk[i], symbol_chunk[i], seq_length, opt2_chunk[i]))
    print('Sequence similarity: {}%\nSequence identity: {}%\n'.format(similarity, identity))

    return opt_align


def fasta_parser(fasta_file):
    with open(fasta_file, 'r') as file:
        sequence_lines = file.read().splitlines()[1:]
    return ''.join(sequence_lines)


# For testing
seqs = ["THRQATWQPPLERMANGRQVE", "RAYMQNDLVKVRYYACHT"]
first_seq = fasta_parser("GLB7A_CHITH.fasta")
second_seq = fasta_parser("GLBE_CHITH.fasta")
sequence_alignment(first_seq, second_seq, 'blosum62.txt', -8, align_type='global', affine=True, ext_penalty=-2)
#sequence_alignment(seqs[0], seqs[1], 'blosum62.txt', -8, align_type='global', affine=True)

# For running in cmd line
# Input Order:
#   Gap penalty
#   Score matrix (e.g. BLOSUM)
#   Sequence 1
#   Sequence 2
#   (Opt) Alignment type (e.g. global or local)
#   (Opt) Affine gap -- True or False (default to False
#   (Opt) Gap extension penalty (only if global chosen), default = -2

# Decide if user input a fasta file or string
# if os.path.splitext(sys.argv[3])[1] == '.fasta':
#     first_seq = fasta_parser(sys.argv[3])
# else:
#     first_seq = sys.argv[3]
#
# if os.path.splitext(sys.argv[4])[1] == '.fasta':
#     second_seq = fasta_parser(sys.argv[4])
# else:
#     second_seq = sys.argv[4]
#
# # Determine if user defined a specific alignment type else global
# if sys.argv[5]:
#     user_align = sys.argv[5]
# else:
#     user_align = 'global'
#
# # Choose affine gaps (Boolean), default is False
# if sys.argv[6]:
#     affine_gap = sys.argv[6]
# else:
#     affine_gap = False
#
# # Input gap extension penalty if provided
# if sys.argv[7]:
#     user_ext_penalty = sys.argv[7]
# else:
#     user_ext_penalty = -2
#
# sequence_alignment(first_seq, second_seq, sys.argv[2], int(sys.argv[1]), align_type=user_align, \
#                    affine=affine_gap, ext_penalty=int(user_ext_penalty))

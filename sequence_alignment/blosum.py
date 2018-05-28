from itertools import combinations
from math import log
from prettytable import PrettyTable
import pandas as pd
import numpy as np
import sys
import os.path


def AA_list(seq_list):
    '''Return a list of all amino acids that appear in a list of sequences'''
    AA_set = set()
    for seq in seq_list:
        for AA in list(seq):
            AA_set.add(AA)
    return AA_set


def AA_count(seq_list):
    '''Return a dictionary with the absolute counts for each amino acid in a list of sequences'''
    all_AA = list(''.join(seq_list))
    AA_counts = {AA:all_AA.count(AA) for AA in AA_list(seq_list)}
    return AA_counts


def AA_prob(seq_list):
    '''Return a dictionary with the probabilities for each amino acid in a list of sequences'''
    abs_counts = AA_count(seq_list)
    total_AA_count = len(''.join(seq_list))
    AA_freqs = {key:value/total_AA_count for (key, value) in abs_counts.items()}

    # Make a nice table
    AA_headers = list(abs_counts.keys())
    table = PrettyTable([" "] + AA_headers)
    table.add_row(["Absolute count"] + list(abs_counts.values()))
    table.add_row((["Probability"] + list(AA_freqs.values())))
    #print(table)
    return AA_freqs


def AA_pair_freq(seq_list):
    '''Return a dictionary with observed probabilities for each amino acid pair in a list of sequences'''
    pairings = list(combinations(seq_list, 2))

    # Get absolute counts for each pair
    AA_pairs = dict()
    for pairs in pairings:
        for i in range(len(pairs[0])):
            #Use sorted() because order should not matter when comparing
            test_pair = ''.join(sorted([pairs[0][i], pairs[1][i]]))
            if test_pair not in AA_pairs.keys():
                AA_pairs[test_pair] = 1
            else:
                AA_pairs[test_pair] += 1

    # Get freq of each pair
    total_AA_pairs = sum(AA_pairs.values())
    AA_pair_freqs = {key:(value/total_AA_pairs) for (key, value) in AA_pairs.items()}

    return AA_pair_freqs


def AA_scores(seq_list, output_table = False):
    '''Return a dictionary with the log odds score for each amino acid pair in a list of sequences'''
    probs = AA_prob(seq_list)
    pair_freqs = AA_pair_freq(seq_list)

    # Create a dictionary which uses the probabilites of the two individual amino acids
    AA_expected = dict()
    for key, value in pair_freqs.items():
        first_aa = list(key)[0]
        second_aa = list(key)[1]
        if first_aa == second_aa:
            AA_expected[key] = probs[first_aa]**2
        else:
            AA_expected[key] = 2*probs[first_aa]*probs[second_aa]

    # Create dictionary of scores
    scores = dict()
    for pair, expected_value in AA_expected.items():
        pair_score = 2*log(pair_freqs[pair]/expected_value, 2)
        if pair_score == 0:
            print("WARNING 0 DETECTED")
        scores[pair] = int(round(pair_score))

    # Print a nice table with pair values if desired
    if output_table:
        i = 0
        chunk_size = 10
        pair_probability_list = [round(value, 3) for value in list(pair_freqs.values())]
        expected_prob_list = [round(value, 3) for value in list(AA_expected.values())]
        score_list = [round(value, 3) for value in list(scores.values())]
        while i < len(pair_freqs.keys()):
            table = PrettyTable([" "] + list(pair_freqs.keys())[i:i+chunk_size])
            table.add_row(["Pair Probs"] + pair_probability_list[i:i+chunk_size])
            table.add_row(["Expected"] + expected_prob_list[i:i+chunk_size])
            table.add_row(["Score"] + score_list[i:i+chunk_size])
            i += chunk_size
            print(table)

    return scores

def score_matrix(seq_list, output_table=False):

    # Generate a score matrix
    aa_list = list(AA_list(seq_list))
    scores = AA_scores(seq_list, output_table)

    # Create empty matrix with proper dimensions
    score_array = np.zeros((len(aa_list), len(aa_list)), dtype='int')  # Empty matrix at first

    # Iterate through pair scores and enter scores into correct positions in array
    for key, score in scores.items():
        AAs = list(key)
        index1 = aa_list.index(AAs[0])
        index2 = aa_list.index(AAs[1])
        score_array[index1][index2] = score
        score_array[index2][index1] = score

    # Format into a nice matrix for output
    score_matrix = pd.DataFrame(score_array, index=aa_list, columns=aa_list)

    return score_matrix


#Test seqs
# seqs = ["TSVKTYAKFVTH", "TSVKTYAKFSTH", "TSVKTYAKFVTH", "LSVKKYPKYVVQ", "SSVKKYPKYSVL"]
# score_matrix(seqs, output_table=True)

with open(sys.argv[1], 'r') as file:
    seqs = file.read().splitlines()

alignment_scores = score_matrix(seqs)

try:
    if os.path.splitext(sys.argv[2])[1] == '.csv':
        alignment_scores.to_csv(sys.argv[2])
    else:
        with open(sys.argv[2], 'w') as output_file:
            alignment_scores.to_string(output_file)
except ValueError:
    print("No valid output path provided. Matrix will not be saved...")
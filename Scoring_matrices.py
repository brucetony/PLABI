from itertools import combinations
from math import log
from prettytable import PrettyTable
import pandas as pd

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
    '''Return a dictionary with absolute counts for every amino acid pair in a list of sequences'''
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
    pairs = AA_pair_freq(seq_list)

    # Create a dictionary which uses the probabilites of the two amino acids and multiples by 2
    AA_expected = {key:(2*probs[list(key)[0]]*probs[list(key)[1]]) for (key, value) in pairs.items()}

    # Create dictionary of scores
    scores = {key: int(round(2 * (log(pairs[key]/value, 2)))) for (key, value) in AA_expected.items()}

    # Print a nice table if desired
    # if output_table:
    #     table = PrettyTable([" "] + list(pairs.keys()))
    #     table.add_row(["Pair Probs"] + list(pairs.values()))
    #     table.add_row(["Expected"] + list(AA_expected.values()))
    #     table.add_row(["Score"] + list(scores.values()))
    #     print(table)

    if output_table:
        tops = list(set(AA[0] for AA in list(scores.keys())))
        side_aa = list(set(AA[0] for AA in list(scores.keys())))

    return scores


#Test seqs
#seqs = ["TSVKTYAKFVTH", "TSVKTYAKFSTH", "TSVKTYAKFVTH", "LSVKKYPKYVVQ", "SSVKKYPKYSVL"]

with open("C:/Users/Bruce/Google Drive/b-it/Programming Lab I/Handout_4/alignment.dat") as file:
    seqs = file.read().splitlines()

a=AA_scores(seqs)
tops = [" "] + list(set(AA[0] for AA in list(a.keys())))
side_aa = list(set(AA[0] for AA in list(a.keys())))
df = pd.DataFrame(tops)
print(df)

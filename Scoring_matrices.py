from itertools import combinations
from math import log

seqs = ["TSVKTYAKFVTH", "TSVKTYAKFSTH", "TSVKTYAKFVTH", "LSVKKYPKYVVQ", "SSVKKYPKYSVL"]

def AA_list(seq_list):
    '''Return a list of all amino acids that appear in a list of sequences'''
    AA_set = set()
    for seq in seq_list:
        for AA in list(seq):
            AA_set.add(AA)
    return AA_set

def AA_count(seq_list):
    '''Return a dictionary with the absolute counts for each amino acid in a list of sequences'''
    AA_counts = {}
    all_AA = list(''.join(seq_list))
    for AA in AA_list(seq_list):
        AA_counts[AA] = all_AA.count(AA)
    return AA_counts

def AA_prob(seq_list):
    '''Return a dictionary with the probabilities for each amino acid in a list of sequences'''
    abs_counts = AA_count(seq_list)
    AA_freqs = {}
    total_AA_count = len(''.join(seq_list))
    for AA in AA_list(seq_list):
        AA_freqs[AA] = abs_counts[AA]/total_AA_count
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

def AA_scores(seq_list):
    '''Return a dictionary with the log odds score for each amino acid pair in a list of sequences'''
    probs = AA_prob(seq_list)
    pairs = AA_pair_freq(seq_list)

    # Create a dictionary which uses the probabilites of the two amino acids and multiples by 2
    AA_expected = {key:(2*probs[list(key)[0]]*probs[list(key)[1]]) for (key, value) in pairs.items()}

    # Create dictionary of scores
    scores = {key:int(round(2*log(pairs[key]/AA_expected[key],2))) for (key, value) in AA_expected.items()}

    return scores

a = AA_scores(seqs)
print(a)

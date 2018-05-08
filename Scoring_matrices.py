from itertools import combinations

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

def AA_freq(seq_list):
    '''Return a dictionary with the frequencies for each amino acid in a list of sequences'''
    abs_counts = AA_count(seq_list)
    AA_freqs = {}
    total_AA_count = len(''.join(seq_list))
    for AA in AA_list(seq_list):
        AA_freqs[AA] = abs_counts[AA]/total_AA_count
    return AA_freqs

def AA_pairs(seq_list):
    '''Return a dictionary with absolute counts for every amino acid pair in a list of sequences'''
    pairings = list(combinations(seq_list, 2))
    AA_pairs = dict()
    for pairs in pairings:
        for i in range(len(pairs[0])):
            #Use sorted() because order should not matter when comparing
            test_pair = ''.join(sorted([pairs[0][i], pairs[1][i]]))
            if test_pair not in AA_pairs.keys():
                AA_pairs[test_pair] = 1
            else:
                AA_pairs[test_pair] += 1

    return AA_pairs

print(AA_pairs(seqs))

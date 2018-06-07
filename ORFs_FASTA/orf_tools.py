import re
from collections import defaultdict


def get_sequence_positions(fasta_file):
    with open(fasta_file, 'r') as f:
        line_list = f.read().split(':')[1:]  # Extract lines after ':' where numbers directly are
        coding_sequences = [re.split(r'[, ]', seq)[0] for seq in line_list]  # Get numbers from line_list
        split_seq_numbers = []
        for seq_set in coding_sequences:
            numbers = seq_set.split('-')  # Remove '-' between numbers and put into tuple
            split_seq_numbers.append((numbers[0], numbers[1]))
        seq_dict = defaultdict(list)  # Create dictionary list to append seq positions to
        for set in split_seq_numbers:
            seq_dict[set[1]].append(set[0])  # Append start position to stop position key in dictionary
    return seq_dict
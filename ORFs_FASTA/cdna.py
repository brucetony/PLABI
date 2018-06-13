import sys
from fasta import single_fasta_sequence, write_fasta


def complement_strand(seq):
    """
    Basic helper function that takes a DNA sequence and returns the reverse complement
    :param seq: A string containing 'ATCG'
    :return: A string containing 'ATCG' and is the reverse complement of the DNA string used as input
    """
    comp_strand = []  # Empty list to add complment bases to
    seq = seq.upper()  # To make sure all letters are upper case
    for base in list(seq):
        if base == 'A':
            comp_strand.append("T")
        elif base == 'C':
            comp_strand.append("G")
        elif base == 'G':
            comp_strand.append("C")
        elif base == 'T' or base == 'U':
            comp_strand.append("A")
    return ''.join(comp_strand[::-1])  # Reverse at end (cDNA often provided in 5' -> 3')


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as in_file:
        hd, seq_of_interest = single_fasta_sequence(in_file)

    with open(sys.argv[2], 'w') as file:
        comp = complement_strand(seq_of_interest)
        hd = "cDNA {}".format(hd)
        write_fasta(file, hd, comp)

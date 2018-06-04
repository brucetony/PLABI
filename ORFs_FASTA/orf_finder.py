import sys
from cdna import complement_strand
from fasta import single_fasta_sequence, write_fasta


def orf_finder(seq):
    seq = seq.upper()
    stop_codon_list = ['TAA', 'TAG', 'TGA']  # List of stop codons
    longest_orfs = []  # List of orf tuples
    for start_pos in range(3):  # Start at position 0, 1, or 2
        k = start_pos
        start_codon = None
        while k < len(seq):
            if seq[k:k+3] == 'ATG' and start_codon is None:  # Mark start codon pos and ignore future start codons
                start_codon = k+1  # Extra 1 because counting starts at 1 in the sequence
                k += 3
            elif seq[k:k+3] in stop_codon_list and start_codon is not None:
                stop_codon = k+4
                longest_orfs.append((start_codon, stop_codon))
                start_codon, stop_codon = None, None
                k += 3
            else:
                k += 3

    return longest_orfs


def orf_writer(seq, outfile):
    cDNAflag = False
    comp_strand = complement_strand(seq)  # Create complementary strand
    orf_lists = [orf_finder(seq), orf_finder(comp_strand)]
    for i in range(len(orf_lists)):
        if i == 1:
            cDNAflag = True
        for orf in orf_lists[i]:
            if cDNAflag:
                header = ':c{}-{}'.format(len(seq)-orf[0]+1, len(seq)-orf[1]+1)
                write_fasta(outfile, header, comp_strand[orf[0]-1:orf[1]-1])
            else:
                header = '{}-{}'.format(orf[0], orf[1])
                write_fasta(outfile, header, seq[orf[0]-1:orf[1]-1])


seq_of_interest = single_fasta_sequence(sys.argv[1])[1]

with open(sys.argv[2], 'w') as file:
    orf_writer(seq_of_interest, file)

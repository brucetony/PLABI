import sys
from cdna import complement_strand
from fasta import single_fasta_sequence, write_fasta


def orf_finder(seq):
    """
    Generator that yields the longest ORF positions
    :param seq: DNA string containing 'ACTG'
    :yield: tuple containing the start and stop positions within the sequence strand for the longest ORF
    """
    seq = seq.upper()
    stop_codon_list = ['TAA', 'TAG', 'TGA']  # List of stop codons
    for start_pos in range(3):  # Start at position 0, 1, or 2
        k = start_pos
        start_codon = None
        while k < len(seq):
            if seq[k:k+3] == 'ATG' and start_codon is None:  # Mark start codon pos and ignore future start codons
                start_codon = k+1  # Extra 1 because counting starts at 1 in the sequence
                k += 3
            elif seq[k:k+3] in stop_codon_list and start_codon is not None:
                stop_codon = k+3
                yield start_codon, stop_codon
                start_codon, stop_codon = None, None
                k += 3
            else:
                k += 3


def orf_writer(seq, outfile, genome_identifier):
    comp_strand = complement_strand(seq)  # Create complementary strand
    genome_identifier = genome_identifier.split(' ')[0]  # Used to removed long name after last '|' in name
    for orf in orf_finder(comp_strand):  # The complementary seq
        header = '{}:c{}-{}'.format(genome_identifier, len(seq) - orf[0] + 1, len(seq) - orf[1] + 1)
        write_fasta(outfile, header, comp_strand[orf[0] - 1:orf[1] - 1])
    for orf in orf_finder(seq):
        header = '{}:{}-{}'.format(genome_identifier, orf[0], orf[1])
        write_fasta(outfile, header, seq[orf[0] - 1:orf[1] - 1])


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as in_file:
        hd, seq_of_interest = single_fasta_sequence(in_file)

    with open(sys.argv[2], 'w') as file:
        orf_writer(seq_of_interest, file, hd)

def single_fasta_sequence(fasta_file):
    """
    :param fasta_file: FASTA formatted file containing exactly one sequence
    :return: Tuple containing the header in position 0 and sequence in position 1
    """
    with open(fasta_file, 'r') as file:
        content = file.read().splitlines()
        header = content[0][1:]  # Remove the '>' character
        sequence = ''.join(content[1:])  # Join sequence lines together
    return (header, sequence)


def fasta_list(fasta_file):
    """
    Same as single_fasta_sequence, only works on a file containing multiple FASTA sequences
    :param fasta_file: FASTA formatted file with 1+ sequences
    :return: List of tuples, each containing the header in position 0 and sequence in position 1
    """
    with open(fasta_file, 'r') as file:
        content = file.read().split('>')[1:]
        genes = []
        for gene in content:
            gene = gene.splitlines()  # Split the lines
            header = gene[0]
            sequence = ''.join(gene[1:]).replace('\n', '')
            genes.append((header, sequence))
    return genes


def fasta_sequences(fasta_file):
    with open(fasta_file, 'r') as file:
        for gene in fasta_list(file):
            yield gene


def write_fasta(outfile, header, sequence):
    outfile.write(">"+header+'\n')
    i = 0
    while i < len(sequence):
        outfile.write(sequence[i:i+69]+'\n')  # Sequence lines cannot be > 70 chars
        i += 69


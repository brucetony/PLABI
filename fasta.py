

def single_fasta_sequence(fasta_file):
    with open(fasta_file, 'r') as file:
        content = file.read().splitlines()
        header = content[0][1:]  # Remove the '>' character
        sequence = ''.join(content[1:])  # Join sequence lines together
    return (header, sequence)


def fasta_list(fasta_file):
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
        for gene in fasta_list(fasta_file):
            yield gene


def write_fasta(outfile, header, sequence):
    with open(outfile, 'w') as file:
        file.write(">"+header+'\n')
        i = 0
        while i < len(sequence):
            file.write(sequence[i:i+69]+'\n')  # Sequence lines cannot be > 70 chars
            i += 69


with open("nudgenudge.faa", "w") as f:
    write_fasta(f,"albatross","WHATFLAVQRISIT")
    write_fasta(f,"lumberjack","ISLEEPALLNIGHTANDIWQRKALLDAY")
    write_fasta(f,"deadparrot","NQRWEGIANPLVE")

# test_hd, test_seq = fasta_list('ecoli-genes.ffn')[1]
# write_fasta('test.ffa', test_hd, test_seq)
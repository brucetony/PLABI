

# Print number of ORFs from orf file
with open('ecoli-orfs.ffn', 'r') as orf_file:
    print('Number of open reading frames:', len(orf_file.read().split('>')[1:]))

with open('ecoli-genes.ffn', 'r') as gene_file:
    print('Number of genes:', len(gene_file.read().split('>')[1:]))
from orf_tools import get_sequence_positions




# Print number of ORFs from orf file
orfs = 'ecoli_orf.ffn'

genes = 'ecoli-genes.ffn'

def predicted_orfs(gene_file, orf_file):
    gene_dict, orf_dict = get_sequence_positions(gene_file), get_sequence_positions(orf_file)  # Make seq position dicts
    gene_starts = [position for sublist in gene_dict.values() for position in sublist]  # Convert list of lists to list
    orf_starts = [position for sublist in orf_dict.values() for position in sublist]
    print(orf_starts)

predicted_orfs(genes, orfs)

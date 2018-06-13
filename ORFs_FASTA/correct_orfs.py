import sys
from orf_tools import get_sequence_positions

# For testing
# orfs = 'ecoli-orfs.ffn'
# genes = 'ecoli-genes.ffn'


def predicted_orfs(orf_file, gene_file, min_orf_length=None):
    print('----------------------------------------------')  # Separator
    # Get number of genes/orfs in each file
    with open(gene_file, 'r') as gene_f:
        num_genes = len(gene_f.read().split('>')[1:])
        print('Number of genes:', num_genes)
    with open(orf_file, 'r') as orf_f:
        num_orfs = len(orf_f.read().split('>')[1:])
        print('Number of open reading frames:', num_orfs)

    gene_dict, orf_dict = get_sequence_positions(gene_file), get_sequence_positions(orf_file)  # Make seq position dicts
    gene_stops, orf_stops = set(gene_dict.keys()), set(orf_dict.keys())

    # TODO Determine where this code goes, here or in counting loop below
    # Remove ORFs smaller than min length from orf_stops list
    if min_orf_length:
        for orf_stop_pos in orf_stops:
            for orf_start_pos in orf_dict[orf_stop_pos]:
                # Remove 'c' from position if present with .replace()
                if abs(int(orf_start_pos.replace('c', '')) - int(orf_stop_pos.replace('c', ''))) < 3 * min_orf_length:
                    orf_dict[orf_stop_pos].remove(orf_start_pos)
                    num_orfs -= 1

        orf_stops = set(entry for entry in orf_stops if len(orf_dict[entry]) != 0)  # Remove empty dict entries

    matching_stop_pos = gene_stops & orf_stops  # Take intersection of both stop pos sets to find matching

    # Find number of ORFs that predict a gene (matching start and stop positions)
    num_orfs_predicting_gene = 0
    for stop_pos in matching_stop_pos:
        for start_pos in orf_dict[stop_pos]:  # Some stop positions have multiple start positions in ORF list
            # if min_orf_length:
            #     # Remove 'c' from position if present with .replace()
            #     if abs(int(start_pos.replace('c', ''))-int(stop_pos.replace('c', ''))) < 3*min_orf_length:
            #         continue  # This means sequence length less than min so skip it
            if start_pos in gene_dict[stop_pos]:
                num_orfs_predicting_gene += 1
    print('Number of ORFs predicting a gene:', num_orfs_predicting_gene)
    print('Ratio of ORFs predicting a gene:', round(num_orfs_predicting_gene/num_orfs, 3))
    print('Number of ORFs with matching gene stop codon:', len(matching_stop_pos))
    print('Ratio of ORFs with matching gene stop codon:', round(len(matching_stop_pos)/num_orfs, 3))
    print('Number of genes with no matching ORF stop codon:', num_genes-len(matching_stop_pos))


# # For testing
# predicted_orfs(genes, orfs, min_orf_length=50)
# predicted_orfs(genes, orfs, min_orf_length=100)
# predicted_orfs(genes, orfs, min_orf_length=150)
# predicted_orfs(genes, orfs, min_orf_length=200)
# predicted_orfs(genes, orfs, min_orf_length=250)
# predicted_orfs(genes, orfs, min_orf_length=300)
# predicted_orfs(genes, orfs, min_orf_length=350)

if __name__ == "__main__":
    if len(sys.argv) > 3:
        predicted_orfs(sys.argv[1], sys.argv[2], min_orf_length=int(sys.argv[3]))
    else:
        predicted_orfs(sys.argv[1], sys.argv[2])
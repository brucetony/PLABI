from orf_tools import get_sequence_positions




# Print number of ORFs from orf file
orfs = 'ecoli-orfs.ffn'

genes = 'ecoli-genes.ffn'

def predicted_orfs(gene_file, orf_file, min_orf_length=None):
    # Get number of genes/orfs in each file
    with open(gene_file, 'r') as gene_f:
        num_genes = len(gene_f.read().split('g')[1:])
        print('Number of genes:', num_genes)
    with open(orf_file, 'r') as orf_f:
        num_orfs = len(orf_f.read().split('>')[1:])
        print('Number of open reading frames:', num_orfs)

    gene_dict, orf_dict = get_sequence_positions(gene_file), get_sequence_positions(orf_file)  # Make seq position dicts
    gene_stops, orf_stops = set(gene_dict.keys()), set(orf_dict.keys())

    # TODO Determine where this code goes, here or in counting loop below
    # Remove ORFs seqs too small here?
    if min_orf_length:
        for orf_stop_pos in orf_stops:
            for orf_start_pos in orf_dict[orf_stop_pos]:
                # Remove 'c' from position if present with .replace()
                if abs(int(orf_start_pos.replace('c', '')) - int(orf_stop_pos.replace('c', ''))) < 3 * min_orf_length:
                    orf_dict[orf_stop_pos].remove(orf_start_pos)
                    num_orfs -= 1

        orf_stops = set([entry for entry in orf_stops if len(orf_dict[entry]) != 0])  # Remove empty dict entries

    matching_stop_pos = gene_stops & orf_stops  # Take intersection of both stop codon sets

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
    print('Number of ORFs with matching stop codon positions:', len(matching_stop_pos))
    print('Ratio of ORFs with matching stop codon positions:', round(len(matching_stop_pos)/num_orfs, 3))
    print('Number of genes with no matching stop codon positions:', num_genes-len(matching_stop_pos))


predicted_orfs(genes, orfs, min_orf_length=350)

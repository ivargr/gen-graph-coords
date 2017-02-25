"""
Interace for interacting with the package OffsetBasedGraphs

Usage example:
$ python3 gen_graph_coords.py grch38.chrom.sizes grch38_alt_loci.txt genes_chr1_GL383518v1_alt.txt

With only two alt loci:
python3 gen_graph_coords.py grch38.chrom.sizes-small grch38_alt_loci_small.txt genes_chr1_GL383518v1_alt.txt

"""

from collections import defaultdict
import sys
import argparse


from methods import *

# Dict struct for holding all arguments taken by the interface
interface = \
{
    'create_graph':
        {
            'help': 'Create graph',
            'arguments':
                [
                    ('chrom_sizes_file_name', 'Tabular file containing two columns, chrom/alt name and size'),
                    ('alt_locations_file_name', 'File containing alternative loci'),
                    ('out_file_name', 'Name of file to store graph and translation objects insize')
                ],
            'method': create_graph
        },


}

# Create parser
parser = argparse.ArgumentParser(
    description='Interact with a graph created from GRCh38')
subparsers = parser.add_subparsers(help='Subcommands')

for command in interface:
    subparser = subparsers.add_parser(command, help=interface[command]["help"])
    for argument, help in interface[command]["arguments"]:
        subparser.add_argument(argument, help=help)
    subparser.set_defaults(func=interface[command]["method"])

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()
if hasattr(args, 'func'):
    args.func(args)
else:
    parser.help()

sys.exit()


"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Interact with a graph created from GRCh38')
    subparsers = parser.add_subparsers(help='Subcommands')

    # Subcommand for create graph
    parser_create_graph = subparsers.add_parser(
        'create_graph', help='Create graph')
    parser_create_graph.add_argument(
        'chrom_sizes_file_name',
        help='Tabular file containing two columns, chrom/alt name and size')
    parser_create_graph.add_argument(
        'alt_locations_file_name',
        help='File containing alternative loci')
    parser_create_graph.add_argument(
        'out_file_name',
        help='Name of file to store graph and translation objects insize')

    parser_create_graph.set_defaults(func=create_graph)

    # Subcommand for genes
    parser_genes = subparsers.add_parser(
        'check_duplicate_genes', help='Check duplicate genes')
    parser_genes.add_argument(
        'translation_file_name',
        help='Translation file created by running create_graph')

    parser_genes.add_argument('genes_file_name', help='Genes')
    parser_genes.set_defaults(func=check_duplicate_genes)

    # Subcommand for merge alt loci using alignments
    parser_merge_alignments = subparsers.add_parser(
        'merge_alignment', help='Merge graph using alignments of alt locus, and save resulting graph to file')

    parser_merge_alignments.add_argument(
        'chrom_sizes_file_name',
        help='Name of chrom sizes file')
    parser_merge_alignments.add_argument(
        'out_file_name',
        help='File name of translation file')
    parser_merge_alignments.add_argument(
        'alt_locus_id', help='Id of alt locus (e.g. chr2_KI270774v1_alt')
    parser_merge_alignments.add_argument(
        'genes', help='Name of genes file (e.g. genes.txt')

    # Subcommand for merge alt loci using alignments
    parser_merge_alignments.set_defaults(func=merge_alignment)

    # Merge all alignments
    parser_merge_all_alignments = subparsers.add_parser(
        'merge_all_alignments',
        help='Merge graph using alignments of ALL alt loci')

    parser_merge_all_alignments.add_argument(
        'chrom_sizes_file_name',
        help='Tabular file containing two columns, chrom/alt name and size')
    parser_merge_all_alignments.add_argument(
        'out_file_name',
        help='File name to store translation object for new graph')
    parser_merge_all_alignments.set_defaults(func=merge_all_alignments)

    # Translate genes to aligned graph
    parser_translate_genes_to_aligned_graph = subparsers.add_parser(
        'translate_genes_to_aligned_graph',
        help='Analyse genes on a merged graph, created by calling merge_all_alignments')

    parser_translate_genes_to_aligned_graph.add_argument(
        'merged_graph_file_name',
        help='Name of file created by running merge_all_alignments')
    parser_translate_genes_to_aligned_graph.add_argument(
        'genes',
        help='Tabular file containing genes')

    parser_translate_genes_to_aligned_graph.add_argument(
        'gene_name',
        help='Name of gene')

    parser_translate_genes_to_aligned_graph.add_argument(
        'out_file_name',
        help='Name of file to write genes to')

    parser_translate_genes_to_aligned_graph.set_defaults(
        func=translate_genes_to_aligned_graph)

    # Analyze multipaht_genes
    parser_analyse_multipath_genes = subparsers.add_parser(
        'analyse_multipath_genes',
        help='Analyse genes on a merged graph, created by calling merge_all_alignments')

    parser_analyse_multipath_genes.add_argument(
        'multipath_genes_file_name',
        help='Name of file generated by translate_genes_to_aligned_graph')
    parser_analyse_multipath_genes.set_defaults(func=analyse_multipath_genes)

    # Analyze multipaht_genes2
    parser_analyse_multipath_genes2 = subparsers.add_parser(
        'analyse_multipath_genes2',
        help='Analyse genes on a merged graph, created by calling merge_all_alignments')

    parser_analyse_multipath_genes2.add_argument(
        'genes_file_name',
        help='Name of gene file (e.g. genes_refseq.txt)')
    parser_analyse_multipath_genes2.add_argument(
        'chrom_sizes_file_name',
        help='Name of file with chrom sizes, used to build graph (e.g. grch38.chrom.sizes)')
    parser_analyse_multipath_genes2.set_defaults(func=analyse_multipath_genes2)

    # Visualize genes
    parser_visualize_genes = subparsers.add_parser(
        'visualize_genes',
        help='Produce html visualization (that can be saved and opened in a browser)')
    parser_visualize_genes.add_argument('translation_file_name',
                                        help='')
    parser_visualize_genes.add_argument('genes_file_name',
                                        help='Pickled genes file')
    parser_visualize_genes.set_defaults(func=visualize_genes)

    # Def visualize alt locus
    parser_visualize_alt_locus = subparsers.add_parser(
        'visualize_alt_locus',
            help='Produce html visualization (that can be saved and opened in a browser)')
    parser_visualize_alt_locus.add_argument('translation_file_name',
            help='Translation with graph to visualize')
    parser_visualize_alt_locus.add_argument('genes',
                                        help='Genes file (e. g. genes_refseq.txt)')
    parser_visualize_alt_locus.add_argument('alt_locus',
                                        help='Alt locus id (e. g. chr2_KI270774v1_alt)')
    parser_visualize_alt_locus.set_defaults(func=visualize_alt_locus)

    # Def visualize alt locus (wrapper)
    parser_visualize_alt_locus_wrapper = subparsers.add_parser(
        'visualize_alt_locus_wrapper',
            help='Produce html visualization (that can be saved and opened in a browser). NB: Wrapper for visualize_alt_locus')
    parser_visualize_alt_locus_wrapper.add_argument('alt_locus',
                                        help='Alt locus id (e. g. chr2_KI270774v1_alt)')
    parser_visualize_alt_locus_wrapper.set_defaults(func=visualize_alt_locus_wrapper)

    # Html alt loci select
    parser_html_alt_loci = subparsers.add_parser(
        'html_alt_loci_select',
            help='Produce html for alt loci select box (only used by web tool)')
    parser_html_alt_loci.set_defaults(func=html_alt_loci_select)


    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.help()

    sys.exit()
"""
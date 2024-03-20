import subprocess
from argparse import Namespace
from logging import Logger


from .util import wf_parser, get_named_logger, create_wd, get_fastq_pass_dir


def run(args: Namespace, l: Logger):
    fastq_pass = get_fastq_pass_dir(args.fastq)
    outdir = create_wd(args.outdir)
    cmd = f"nextflow run epi2me-labs/wf-metagenomics --fastq {fastq_pass} --out_dir {outdir} --analyse_unclassified {args.unclassified} --database_set {args.db} --min_len {args.length} --min_read_qual {args.quality} --threads {args.threads} --n_taxa_barplot {args.taxa}"
    l.info(f"Running workflow: {cmd}")
    run = subprocess.run(
            cmd,
            shell=True
            )
    
def main(args: Namespace):
    logger = get_named_logger("microbiome")
    
    run(args, logger)
    
def argparser():
    """Argument parser for entrypoint."""
    parser = wf_parser("microbiome")
    parser.add_argument('-i', '--fastq-dir', 
                            dest='fastq', required=True,
                            help="path to fastq_pass directory",
                            type=str
                            )
    parser.add_argument('-o', '--outdir', 
                            dest='outdir', required=True,
                            help="Path to output directory",
                            type=str,
                            )
    parser.add_argument("-d", "--database",
                            dest="db", default="ncbi_16s_18s",
                            help="Database to use. (default: PlusPFP-8)",
                            type=str,
                            )
    parser.add_argument("-t", "--threads",
                            dest='threads', default=8,
                            help="Number of threads to use. (default: 8)",
                            type=int,
                            )
    parser.add_argument("-n", "--n-taxa",
                            dest='taxa', default=9,
                            help="Number of most abundant taxa to display in barplot, the rest will be grouped as 'other'. (default: 9)",
                            type=int,
                            )
    parser.add_argument("-l", "--min-len",
                            dest='length', default=1200,
                            help="Lower read length limit. (default: 1200)",
                            type=int,
                            )
    parser.add_argument('-q', '--min-qual',
                            dest='quality', default=9,
                            help="Lower read quality limit. (default: 9)",
                            type=int,
                            )
    parser.add_argument('-u', "--unclassified",
                        dest='unclassified', default=False,
                        help="Analyse unclassfied reads",
                        type=bool,
                        )
    return parser
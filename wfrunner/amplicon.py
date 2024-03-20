import subprocess
from argparse import Namespace
from logging import Logger

from .util import wf_parser, get_named_logger, create_wd, get_fastq_pass_dir


def run(args: Namespace, l: Logger):
    fastq_pass = get_fastq_pass_dir(args.fastq)
    outdir = create_wd(args.outdir)
    cmd = f"nextflow run epi2me-labs/wf-amplicon --fastq {fastq_pass} --out_dir {outdir} --analyse_unclassified {args.unclassified} --min_read_length {args.length} --min_read_qual {args.quality} --threads {args.threads} --reference {args.reference}"
    l.info(f"Running workflow: {cmd}")
    run = subprocess.run(
            cmd,
            shell=True
            )
    
def main(args: Namespace):
    logger = get_named_logger("amplicon")
    
    run(args, logger)
    
def argparser():
    """Argument parser for entrypoint."""
    parser = wf_parser("amplicon")
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
    parser.add_argument("-t", "--threads",
                            dest='threads', default=8,
                            help="Number of threads to use. (default: 8)",
                            type=int,
                            )
    parser.add_argument("-l", "--min-len",
                            dest='length', default=100,
                            help="Lower read length limit. (default: 100)",
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
    parser.add_argument('-r', "--reference",
                        dest="reference", default='',
                        help="Path to reference",
                        type=str,
                        )
    return parser
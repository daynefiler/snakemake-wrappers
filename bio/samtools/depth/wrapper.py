"""Snakemake wrapper for running samtools depth."""

__author__ = "Dayne L Filer"
__copyright__ = "Copyright 2020, Dayne L Filer"
__email__ = "dayne.filer@gmail.com"
__license__ = "MIT"

from snakemake.shell import shell

# Samtools takes additional threads through its option -@
# One thread for samtools merge
# Other threads are *additional* threads passed to the '-@' argument
threads = "" if snakemake.threads <= 1 else " -@ {} ".format(snakemake.threads - 1)

# check for optional bed file
bed = "" if snakemake.bed == "" else "-b {}".format(snakemake.input.bed)

shell(
    "samtools depth {threads} {snakemake.params} {bed} "
    "-o {snakemake.output[0]} {snakemake.input.bams}"
)

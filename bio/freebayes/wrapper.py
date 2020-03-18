__author__ = "Johannes Köster"
__copyright__ = "Copyright 2017, Johannes Köster"
__email__ = "johannes.koester@protonmail.com"
__license__ = "MIT"


from snakemake.shell import shell

shell.executable("bash")

log = snakemake.log_fmt_shell(stdout=False, stderr=True)

params = snakemake.params.get("extra", "")

pipe = ""
if snakemake.output[0].endswith(".bcf"):
    pipe = "| bcftools view -Ob -"

# check for optional bed file
targets = snakemake.input.get("targets", "")
if targets:
    targets = "--targets " + target

# check for optional cnvMap file
cnv = snakemake.input.get("cnvMap", "")
if cnv:
    cnv = "--cnv-map " + cnv

# check for optional populations file
pop = snakemake.input.get("populations", "")
if pop:
    known = "--populations " + populations

if snakemake.threads == 1:
    freebayes = "freebayes"
else:
    chunksize = snakemake.params.get("chunksize", 100000)
    freebayes = (
        "freebayes-parallel <(fasta_generate_regions.py "
        "{snakemake.input.ref}.fai {chunksize}) "
        "{snakemake.threads}"
    ).format(snakemake=snakemake, chunksize=chunksize)

shell(
    "({freebayes} {targets} {cnv} {pop} {params} -f {snakemake.input.ref}"
    " {snakemake.input.samples} {pipe} > {snakemake.output[0]}) {log}"
)

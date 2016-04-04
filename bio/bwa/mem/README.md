# Wrapper for bwa mem.

## Example:

```
rule bwa_mem:
    input:
        ref="genome.fasta",
        sample=["reads/{sample}.1.fastq.gz", "reads/{sample}.2.fastq.gz"]
    output:
        "mapped/{sample}.bam"
    log:
        "logs/bwa_mem/{sample}.log"
    params:
        "-R '@RG\tID:{sample}\tSM:{sample}'"  # optional parameters for bwa mem (e.g. read group)
    threads: 8
    wrapper:
        "0.2.0/bio/bwa/mem"
```
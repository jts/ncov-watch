# ncov watch

Screen for mutations of interest in SARS-CoV-2 sequencing results

## Installation

```
python setup.py install
```

## Usage

This script will recursively search a directory structure for variants files (ivar `variant.tsv` files, or nanopore `.pass.vcf.gz` files) and print out any samples that match a variant in a defined "watchlist" VCF file. For example this command will search for samples that contain one of the mutations defining the B.1.1.7 variant:

```
ncov-watch --mutation_set uk_variant --directory data 2>/dev/null
```

Alternatively you can pass the variant files on stdin:

```
find data/ -name "*.variants.tsv" | ncov-watch -m uk_variant 2>/dev/stderr
```

(note `2>/dev/stderr` is to silence pysam warnings when parsing VCF files). 

The built-in watchlists can be seen [here](https://github.com/jts/ncov-watch/tree/master/ncov_watch/watchlists). You can also use your own watchlist by providing `-m` with the path to a local VCF. 

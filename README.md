# ncov watch

Screen for mutations of interest in SARS-CoV-2 sequencing results

## Installation

```
python setup.py install
```

## Usage

This script will recursively search a directory structure for variants files (ivar `variant.tsv` files, or nanopore `.pass.vcf.gz` files) and print out any samples that match a variant in `watchlist.vcf`. Example:

```
ncov-watch --watchlist /path/to/watchlist.vcf --directory data 2>/dev/null
```

Alternatively you can pass the variant files on stdin:

```
find data/ -name "*.variants.tsv" | python ncov-watch.py --watchlist /path/to/watchlist.vcf 2>/dev/stderr
```

(note `2>/dev/stderr` is to silence pysam warnings when parsing VCF files)

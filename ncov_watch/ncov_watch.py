#!/usr/bin/env python

import argparse
import pysam
import sys
import csv
import os
import pkg_resources
from pathlib import Path

class Variant:
    def __init__(self, contig, position, reference, alt):
        self.contig = contig
        self.position = position
        self.reference = reference
        self.alt = alt
        self.name = "unnamed"

    def key(self):
        return ",".join([str(x) for x in [self.contig, self.position, self.reference, self.alt]])

class SummaryOutput:
    def write_header():
        print("sample\tmutations")

    def write_variants(sample_name, variants):
        out = list()
        for v in variants:
            sample_variant = v[0]
            watch_variant = v[1]
            out.append(watch_variant.name)
        print("\t".join([sample_name, ",".join(out)]))

class MutationOutput:
    def write_header():
        print("\t".join(["sample", "mutation", "contig", "position", "reference", "alt"]))

    def write_variants(sample_name, variants):
        for v in variants:
            sample_variant = v[0]
            watch_variant = v[1]
            print("\t".join([sample_name, watch_variant.name, sample_variant.contig, str(sample_variant.position), sample_variant.reference, sample_variant.alt]))
 
def load_vcf(filename):
    variants = list()
    f = pysam.VariantFile(filename,'r')
    for record in f:
        if len(record.alts) > 1:
            sys.stderr.write("Multi-allelic VCF not supported\n")
            sys.exit(1)


        v = Variant(record.chrom, record.pos, record.ref, record.alts[0])
        if "Name" in record.info:
            v.name = record.info["Name"]
        variants.append(v)

    return variants

def load_ivar_variants(filename):
    variants = list()
    try:
        with open(filename, 'r') as ifh:
            reader = csv.DictReader(ifh, delimiter='\t')
            for record in reader:
                ref = record["REF"]
                alt = record["ALT"]
                if alt[0] == "-":
                    ref += alt[1:]
                    alt = ref[0]
                elif alt[0] == "+":
                    alt = ref + alt[1:]

                variants.append(Variant(record["REGION"], record["POS"], ref, alt))
    except:
        pass
    return variants

def get_from_directory(directory):
    find_files = lambda pattern : [ path for path in Path(directory).rglob(pattern) ]
    files = find_files("*pass.vcf") + find_files("*pass.vcf.gz") + find_files("*variants.tsv")
    for f in files:
        yield str(f)

def get_from_stdin():
    for line in sys.stdin:
        yield line.rstrip()

def main():

    description = 'Report samples containing a variant in the watchlist'
    parser = argparse.ArgumentParser(description=description)

    # get preinstalled mutation sets
    mutation_sets = pkg_resources.resource_listdir(__name__, 'watchlists')
    mutation_sets = [Path(mutation_set).stem for mutation_set in mutation_sets]

    parser.add_argument('-m', '--mutation_set', required=True,
            help=f"Either one of the preinstalled mutation sets: {mutation_sets}\n"
                  "or a full path to a VCF file containing mutations")
    parser.add_argument('-d', '--directory', help='root of directories holding variant files')
    parser.add_argument('-s', '--output-style', help='style of output either mutation (default) or summary', default="mutation")
    args = parser.parse_args()

    # if the argument provided is in the preinstalled mutation sets use
    # as appropriate
    if args.mutation_set in mutation_sets:
        mutation_set_path = Path("watchlists") / Path(args.mutation_set + ".vcf")
        mutation_set = pkg_resources.resource_filename(__name__, str(mutation_set_path))
    else:
        # otherwise check if the mutation vcf exists
        mutation_set_path = Path(args.mutation_set)
        if mutation_set_path.is_file():
            mutation_set = args.mutation_set
        else:
            # if it doesn't exist then print error, help, and exit with non-zero
            print("Provided mutation set: {mutation_set_path} does not exist",
                  file=sys.stderr)
            parser.print_help()
            sys.exit(1)

    watch_variants = load_vcf(mutation_set)
    watch_dict = dict()
    for v in watch_variants:
        watch_dict[v.key()] = v

    input_files = get_from_stdin()
    if args.directory:
        input_files = get_from_directory(args.directory)

    if args.output_style == "summary":
        output = SummaryOutput
    elif args.output_style == "mutation":
        output = MutationOutput
    else:
        sys.stderr.write("Unknown output style: %s" % (args.output_style))
        sys.exit(1)

    output.write_header()

    for f in input_files:
        if f.find("variants.tsv") >= 0:
            variants = load_ivar_variants(f)
        else:
            variants = load_vcf(f)
        
        matches = list()
        for v in variants:
            if v.key() in watch_dict:
                matches.append( (v, watch_dict[v.key()]) )
        
        if len(matches) > 0:
            output.write_variants(os.path.basename(f), matches)

if __name__ == "__main__":
    main()

#! /usr/bin/env python3
import dboost
import sys
import utils
import features
import argparse
import cli
from utils.parsing import autoconv
from utils.print import print_rows

dataset = []
row_length = None

parser = argparse.ArgumentParser(parents = [cli.get_base_parser()],
                                 description="Loads a database from a text file, and reports outliers")
parser.add_argument("input", nargs='?', default = "-", type=argparse.FileType('r'))

args = parser.parse_args()

for line in args.input:
    line = line.strip().split(args.fs)
    
    if row_length != None and len(line) != row_length:
        sys.stderr.write("Discarding {}\n".format(line))

    row_length = len(line)
    dataset.append(tuple(autoconv(field) for field in line))

print(args)
models = cli.load_models(args)

for model in models:
    outliers = dboost.outliers_static(dataset, model)

    if len(outliers) == 0:
        print("   All clean!")
    else:
        print_rows(outliers, model, features.descriptions(features.rules), args.verbosity)

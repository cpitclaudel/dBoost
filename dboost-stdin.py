#! /usr/bin/env python3
import dboost
import sys
import utils
import features
import argparse
import cli
import itertools 
from utils.autoconv import autoconv
from utils.print import print_rows

dataset = []
testset = []

def process_file(f,d):
  row_length = None
  for line in f: 
      line = line.strip().split(args.fs)
    
      if row_length != None and len(line) != row_length:
          sys.stderr.write("Discarding {}\n".format(line))

      row_length = len(line)
      d.append(tuple(autoconv(field) for field in line))

parser = cli.get_sdtin_parser()
args, models, preprocessors, rules = cli.parsewith(parser)

process_file(args.input,dataset)
if args.test_input is not None:
  process_file(args.test_input,testset)

for preprocessor, model in itertools.product(preprocessors, models):
    outliers = dboost.outliers_static(dataset, preprocessor, model, rules, testset)

    if len(outliers) == 0:
        print("   All clean!")
    else:
        print_rows(outliers, model, preprocessor.hints,
                   features.descriptions(rules), args.verbosity)

#! /usr/bin/env python3
import dboost
import sys
import utils
import features
import argparse
import cli
import itertools 
from utils.read import stream_tuples 
from utils.autoconv import autoconv
from utils.print import print_rows

parser = cli.get_sdtin_parser()
args, models, preprocessors, rules = cli.parsewith(parser)

testset_generator = stream_tuples(args.input, args.fs, args.floats_only, args.inmemory)

if args.trainwith == None:
    args.trainwith = args.input
    trainset_generator = testset_generator
else:
    trainset_generator = stream_tuples(args.trainwith, args.fs, args.floats_only, args.inmemory)

if not args.inmemory and not args.trainwith.seekable():
    raise ArgumentError("Input does not support streaming. Try using --inmemory?")

# TODO: Input should be fed to all models in one pass.
for model in models:
    for preprocessor in preprocessors:
        outliers = list(dboost.outliers(trainset_generator, testset_generator,
                                        preprocessor, model, rules))

        if len(outliers) == 0:
            print("   All clean!")
        else:
            print_rows(outliers, model, preprocessor.hints,
                       features.descriptions(rules), args.verbosity)

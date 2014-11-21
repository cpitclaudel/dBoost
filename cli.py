import argparse
from models import gaussian, discrete

REGISTERED_MODELS = (gaussian.Simple, gaussian.Mixture, discrete.Histogram)

def get_base_parser():
    base_parser = argparse.ArgumentParser(add_help = False)
    base_parser.add_argument("-F", "--field-separator", nargs = 1, dest = "fs",
                             action = "store", default = "\t")

    base_parser.add_argument("-v", "--verbose", dest = "verbosity",
                             action = "store_const", const = 1, default = 0)

    base_parser.add_argument("-vv", "--debug", dest = "verbosity",
                             action = "store_const", const = 2)
    
    for model in REGISTERED_MODELS:
        model.register(base_parser)

    return base_parser

def get_sdtin_parser():
    parser = argparse.ArgumentParser(parents = [get_base_parser()],
                                     description="Loads a database from a text file, and reports outliers")
    parser.add_argument("input", nargs='?', default = "-", type=argparse.FileType('r'))
    return parser

def get_mimic_parser():
    parser = argparse.ArgumentParser(parents = [get_base_parser()],
                                     description="Loads the mimic2 database using sqlite3, and reports outliers")
    parser.add_argument("path")
    return parser

def load_models(namespace):
    models = []
    for model in REGISTERED_MODELS:
        params = getattr(namespace, model.ID)
        if params != None:
            models.append(model.from_parse(params))
    return models

def parsewith(parser):
    args = parser.parse_args()
    models = load_models(args)
    if len(models) == 0:
        parser.error("No model specified!")
    return args, models

import argparse
import features
from preprocessors import statistical
from models import gaussian, discrete 

REGISTERED_MODELS = (gaussian.Simple, gaussian.Mixture, discrete.Histogram)
REGISTERED_PREPROCESSORS = (statistical.Pearson,)

def register_modules(parser, modules):
    for module in modules:
        module.register(parser)

def get_base_parser():
    base_parser = argparse.ArgumentParser(add_help = False)
    base_parser.add_argument("-v", "--verbose", dest = "verbosity",
                             action = "store_const", const = 1, default = 0,
                             help = "Print basic debugging information.")

    base_parser.add_argument("-vv", "--debug", dest = "verbosity",
                             action = "store_const", const = 2,
                             help = "Print advanced debugging information.")

    base_parser.add_argument("-d", "--disable-rule", dest = "disabled_rules",
                             action = "append", metavar = 'rule',
                             help = "Disable a rule.")

    base_parser.add_argument("-tr", "--train_data", dest = "train_input",
                             type = argparse.FileType('r'),
                             help = "Data to train the models on.")

    base_parser.add_argument("-te", "--test_data", dest = "test_input",
                             type = argparse.FileType('r'),
                             help = "Data to generate outliers from.")

    base_parser.set_defaults(disabled_rules = [])

    register_modules(base_parser, REGISTERED_MODELS)
    register_modules(base_parser, REGISTERED_PREPROCESSORS)
    
    return base_parser

def get_sdtin_parser():
    parser = argparse.ArgumentParser(parents = [get_base_parser()],
                                     description="Loads a database from a text file, and reports outliers")
    parser.add_argument("input", nargs='?', default = "-", type = argparse.FileType('r'),
                        help = "Read data from file input. If omitted or '-', read from standard input.")
    
    parser.add_argument("-F", "--field-separator", dest = "fs",
                        action = "store", default = "\t", metavar = "fs",
                        help = "Use fs as the input field separator (default: tab).")

    return parser

def get_mimic_parser():
    parser = argparse.ArgumentParser(parents = [get_base_parser()],
                                     description="Loads the mimic2 database using sqlite3, and reports outliers")
    parser.add_argument("db", help = "Read data from sqlite3 database file db.")
    return parser

def load_modules(namespace, parser, registered_modules):
    modules = []

    for module in registered_modules:
        params = getattr(namespace, module.ID)
        if params != None:
            modules.append(module.from_parse(params))
            
    if len(modules) == 0:
        args = ["'--" + module.ID + "'" for module in registered_modules]
        parser.error("Please specify one of [{}]".format(", ".join(args)))
            
    return modules

def parsewith(parser):
    args = parser.parse_args()
    
    models = load_modules(args, parser, REGISTERED_MODELS)
    preprocessors = load_modules(args, parser, REGISTERED_PREPROCESSORS)
    
    disabled_rules = set(args.disabled_rules)
    available_rules = set(r.__name__ for rs in features.rules.values() for r in rs)
    invalid_rules = disabled_rules - available_rules
    if len(invalid_rules) > 0:
        parser.error("Unknown rule(s) {}".format(", ".join(sorted(invalid_rules))))
    rules = {t: [r for r in rs if r.__name__ not in disabled_rules]
             for t, rs in features.rules.items()}

    return args, models, preprocessors, rules

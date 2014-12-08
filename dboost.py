#! /usr/bin/env python3
import sys
import utils
import features
from itertools import chain

def expand_field(f, rules):
    rls = rules[type(f)]
    return tuple(chain.from_iterable(rule(f) for rule in rls))

def expand(x, rules):
    return tuple(expand_field(f, rules) for f in x)

def expand_stream(generator, rules, keep_x):
    for x in generator():
        X = expand(x, rules)
        yield (x, X) if keep_x else X 

def outliers_static(dataset, preproc, model, rules):
    dataset = list(dataset)
    datasetc = list(zip(*dataset))
    # Collect stats in preprocessor
    preproc.fit(expand_stream(lambda: datasetc, rules, False))
    print(preproc.hints)
    return list(outliers_streaming(lambda: dataset, preproc, model, rules))

def outliers_streaming(generator, preproc, model, rules):
    print(">> Building model...")
    model.fit(expand_stream(generator, rules, False))

    print(">> Finding outliers...")
    for index, (x, X) in enumerate(expand_stream(generator, rules, True)):
        _discrepancies = model.find_discrepancies(X, index)
        if len(_discrepancies) > 0:
            yield (x, X, _discrepancies)

#! /usr/bin/env python3
import sys
import utils
import features
from itertools import chain

def expand_field(f): # TODO: Should features be kept grouped by rule? # C: I'd say yes probably, even if they get flattened in certain models
    rls = features.rules[type(f)]
    return tuple(chain.from_iterable(rule(f) for rule in rls))

def expand(x):
    return tuple(expand_field(f) for f in x)

def find_correlation(Xs):
	for (nb, X) in enumerate(Xs):
		print(X)

def expand_stream(generator, keep_x):
    for x in generator():
        X = expand(x)
        yield (x, X) if keep_x else X 

def correlation(dataset):
	dataset = list(dataset)
	find_correlation(expand_stream((lambda: dataset), False))

def outliers_static_stats(dataset, model):
    dataset = list(dataset)
    datasetc = list(zip(*dataset))
    outliers_streaming_stats_bm(lambda: datasetc, model)
    return list(outliers_streaming_stats_fo(lambda: dataset, model))

def outliers_streaming_stats_bm(generator, model):
    print(">> Building model...")
    model.fit(expand_stream(generator, False),expand_stream(generator, False))

def outliers_streaming_stats_fo(generator, model):
    print(">> Finding outliers...")
    for index, (x, X) in enumerate(expand_stream(generator, True)):
        _discrepancies = model.find_discrepancies(X, index)
        if len(_discrepancies) > 0:
            yield (x, X, _discrepancies)
 
def outliers_static(dataset, model):
    dataset = list(dataset)
    return list(outliers_streaming(lambda: dataset, model))

def outliers_streaming(generator, model):
    print(">> Building model...")
    model.fit(expand_stream(generator, False))

    print(">> Finding outliers...")
    for index, (x, X) in enumerate(expand_stream(generator, True)):
        _discrepancies = model.find_discrepancies(X, index)
        if len(_discrepancies) > 0:
            yield (x, X, _discrepancies)
 
def print_outliers(dataset):
    from models import gaussian
    model = gaussian.mixture(2)
    outliers, _, failed_tests = zip(*outliers_static(dataset, model))
    utils.print_rows(outliers, failed_tests, features.rules)

#! /usr/bin/env python3
import sys
import utils
import features
from itertools import chain

def expand_field(f, rules): # TODO: Should features be kept grouped by rule? # C: I'd say yes probably, even if they get flattened in certain models
    rls = rules[type(f)]
    return tuple(chain.from_iterable(rule(f) for rule in rls))

def expand(x, rules):
    return tuple(expand_field(f, rules) for f in x)

def find_correlation(Xs): # TODO
	for (nb, X) in enumerate(Xs):
		print(X)

def expand_stream(generator, rules, keep_x):
    for x in generator():
        X = expand(x, rules)
        yield (x, X) if keep_x else X 

def correlation(dataset): # TODO
	dataset = list(dataset)
	find_correlation(expand_stream((lambda: dataset), False))

<<<<<<< HEAD
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
=======
def outliers_static(dataset, model, rules):
>>>>>>> 6208414dc6fe4ba508429ed15ce5640f4eb643c8
    dataset = list(dataset)
    return list(outliers_streaming(lambda: dataset, model, rules))

def outliers_streaming(generator, model, rules):
    print(">> Building model...")
    model.fit(expand_stream(generator, rules, False))

    print(">> Finding outliers...")
    for index, (x, X) in enumerate(expand_stream(generator, rules, True)):
        _discrepancies = model.find_discrepancies(X, index)
        if len(_discrepancies) > 0:
            yield (x, X, _discrepancies)

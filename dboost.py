#! /usr/bin/env python3
import sys
import utils
import features

UPPERCASE, LOWERCASE, TITLECASE = 1, 2, 3
NUM = 1

from itertools import chain

def expand_field(f): # TODO: Should features be kept grouped by rule? # C: I'd say yes probably, even if they get flattened in certain models
    rls = features.rules[type(f)]
    return tuple(chain.from_iterable(rule(f) for rule in rls))

def expand(x):
    return tuple(expand_field(f) for f in x)

def find_correlation(Xs):
	for (nb, X) in enumerate(Xs):
		print(X)

# pearson correlation coefficient
# http://stackoverflow.com/questions/3949226/calculating-pearson-correlation-and-significance-in-python
def pearson_r(x,y):
	assert len(x) == len(y)
	n = len(x)
	assert n > 0
	avg_x = float(sum(x)) / n 
	avg_y = float(sum(y)) / n
	diffprod = 0
	xdiff2 = 0
	ydiff2 = 0
	for idx in range(n):
		xdiff = x[idx] - avg_x
		ydiff = y[idx] - avg_y
		diffprod += xdiff * ydiff
		xdiff2 += xdiff * xdiff
		ydiff2 += ydiff * ydiff
	return diffprod / sqrt(xdiff2 * ydiff2)

def expand_stream(generator, keep_x):
    for x in generator():
        X = expand(x)
        yield (x, X) if keep_x else X 

def correlation(dataset):
	dataset = list(dataset)
	find_correlation(expand_stream((lambda: dataset), False))

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

#! /usr/bin/env python3
import sys
import utils
import features
from utils import tupleops
from itertools import chain

def expand_field(f, rules):
    rls = rules[type(f)]
    return tuple(chain.from_iterable(rule(f) for rule in rls))

def expand(x, rules):
    return tuple(expand_field(f, rules) for f in x)

def expand_hints(X, hints):
    expanded_hints = tupleops.deepmap(lambda h: X[h[0]][h[1]], hints)
    #if not expanded_hints:
    #  return X
    return (expanded_hints,) + X

def expand_stream(generator, rules, keep_x, hints = ()):
    for x in generator():
        X = expand(x, rules)
        #if hints:
        X = expand_hints(X, hints)
        yield (x, X) if keep_x else X 

def parse_discrepancies(x, X, discrepancies, hints):
    parsed = []

    for (index, subindices) in discrepancies:
        # TODO: In the long run, in might be better to adjust models to directly
        # return outliers in this format
        parsed.extend(((index, subindex),) for subindex in subindices)

    return (x, X, parsed)
        
def outliers_static(dataset, preprocessor, model, rules):
    dataset = list(dataset)
    return list(outliers_streaming(lambda: dataset, preprocessor, model, rules))

def outliers_streaming(generator, preprocessor, model, rules):
    #TODO: Models shouldn't be applied one by one
    
    print(">> Finding correlations")
    preprocessor.fit(expand_stream(generator, rules, False))
    print(preprocessor.hints)
    
    print(">> Building model...")
    model.fit(expand_stream(generator, rules, False,preprocessor.hints))

    print(">> Finding outliers...")
    for index, (x, X) in enumerate(expand_stream(generator, rules,
                                                 True, preprocessor.hints)):
        discrepancies = model.find_discrepancies(X, index)
        if len(discrepancies) > 0:
            yield parse_discrepancies(x, X, discrepancies, preprocessor.hints)

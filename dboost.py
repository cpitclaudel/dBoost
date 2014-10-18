#! /usr/bin/env python3
import unicodedata
import time
from math import sqrt
import sys
import utils

UPPERCASE, LOWERCASE, TITLECASE = 1, 2, 3
NUM = 1

def string_normalize(s): # http://stackoverflow.com/questions/517923/
   return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def string_case(s):
    return (s.isupper(), s.islower(), s.istitle())

def string_domain(s):
    return (s.isdigit(),)

def bits(*positions):
    def rule(i):
        return ((i >> pos) & 1 for pos in positions)
    return rule

def mod(*mods):
    def rule(i):
        return (i % mod for mod in mods)
    return rule

DATE_PROPS = "tm_year", "tm_mon", "tm_mday", "tm_hour", "tm_min", "tm_sec", "tm_wday", "tm_yday"
def unix2date(timestamp):
    t = time.gmtime(timestamp)
    return map(lambda a: getattr(t, a), DATE_PROPS)

def length(o):
    return (len(o),)

rules = {
    str: (string_case, string_domain, length),
    int: (bits(0, 1, 2, 3, 4, 5), mod(10), unix2date)
}

from itertools import chain

def expand_field(f):
    rls = rules.get(type(f), [])
    return tuple(chain.from_iterable(rule(f) for rule in rls))

def expand(x):
    return tuple(expand_field(f) for f in x)

def zeroif(S, X):
    return S if S != None else tuple(tuple(0 for _ in x) for x in X)

def root(X):
    return tuple(tuple(sqrt(xi) for xi in x) for x in X)

def merge(S, X, f, phi):
    return tuple(tuple(phi(si, f(xi)) for si, xi in zip(s, x)) for s, x in zip(S, X))

def id(x):
    return x

def sqr(x):
    return x * x if x != None else None

def not_null(x):
    return x != None

def plus(a, b):
    return a + b if b != None else a

def minus(a, b):
    return a - b if b != None else a

def mul(a, b):
    return a * b if b != None else a

def div0(a, b):
    return a / b if a != None and b != 0 else 0

def tuplify(a, b):
    return (a, b)

def report_progress(nb):
    if nb % 1000 == 0:
        sys.stderr.write(str(nb) + "\r")

def gaussian_model(Xs):
    S, S2, C = None, None, None

    for (nb, X) in enumerate(Xs):
        report_progress(nb)
        S, S2, C = zeroif(S, X), zeroif(S2, X), zeroif(C, X)
        S = merge(S, X, id, plus)
        S2 = merge(S2, X, sqr, plus)
        C = merge(C, X, not_null, plus)
    
    SAVG = merge(S, C, id, div0)
    SAVG2 = merge(SAVG, SAVG, id, mul)
    S2AVG = merge(S2, C, id, div0)
    
    VAR = merge(S2AVG, SAVG2, id, minus)
    SIGMA = root(VAR)

    return merge(SAVG, SIGMA, id, tuplify)

def test_one(xi, gaussian):
    avg, sigma = gaussian
    return abs(xi - avg) <= 3 * sigma

def first_discrepancy(X, gaussian):
    for field_id, (x, m) in enumerate(zip(X, gaussian)):
        if not all(test_one(xi, mi) for xi, mi in zip(x, m)):
            return field_id
    return None

def discrepancies(X, gaussian):
    ret = []
    for field_id, (x, m) in enumerate(zip(X, gaussian)):
        if not all(test_one(xi, mi) for xi, mi in zip(x, m)):
            ret.append(field_id)
    return ret
    
def test(X, gaussian):
    return (first_discrepancy(X, gaussian) != None)

def expand_stream(generator, keep_x):
    for x in generator():
        X = expand(x)
        yield (x, X) if keep_x else X 

def outliers_static(dataset):
    dataset = list(dataset)
    return list(outliers_streaming(lambda: dataset))

def outliers_streaming(generator):
    print(">> Building model...")
    model = gaussian_model(expand_stream(generator, False))

    print(">> Finding outliers...")
    for x, X in expand_stream(generator, True):
        _discrepancies = discrepancies(X, model)
        if len(_discrepancies) > 0:
            yield (x, X, _discrepancies)

def print_outliers(dataset):
    outliers, _, highlights = zip(*outliers_static(dataset))
    utils.print_rows(outliers, highlights)

import sys
from math import sqrt
from itertools import chain

def defaultif(S, X, default):
    return S if S != None else tuple(tuple(default() for _ in x) for x in X)

def zeroif(S, X):
    return S if S != None else tuple(tuple(0 for _ in x) for x in X)

def root(X):
    return deepmap(sqrt, X) #TODO remove

def deepmap(f, X):
    return tuple(tuple(f(xi) for xi in x) for x in X)

def filter(f, X):
    return tuple(tuple((xi if (xi != None and f(xi)) else None) for xi in x) for x in X)

def merge(S, X, f, phi):
    return tuple(tuple(phi(si, f(xi)) for si, xi in zip(s, x)) for s, x in zip(S, X))

def deepapply(S, X, f):
    for s, x in zip(S, X):
        for si, xi in zip(s, x):
            f(si, xi)

def number(X):
    return tuple(tuple((i, j) for j, _ in enumerate(x)) for i, x in enumerate(X))

def id(x):
    return x

def sqr(x):
    return x * x if x != None else None

def not_null(x):
    return x != None

def keep_if(a, b):
    return a if b else None

def plus(a, b):
    return a + b if b != None else a

def minus(a, b):
    return a - b if b != None else a

def mul(a, b):
    return a * b if b != None else a

def div0(a, b):
    return a / b if a != None and b != 0 else 0

def incrkey(a, b):
    if a != None:
        a[b] += 1
    return a

def tuplify(a, b):
    return (a, b)

def flatten(tup):
    return list(chain(*tup))

def filter_abc(X, abc):
    return tuple(tuple(xi for xi in x if isinstance(xi, abc)) for x in X)

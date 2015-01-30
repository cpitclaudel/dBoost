import numbers
from collections import Counter
from itertools import combinations
from utils import tupleops
from utils.print import debug

class DiscreteStats:
    ID = "discretestats"

    def __init__(self, max_buckets, fundep_size):
        self.max_buckets = max_buckets
        self.fundep_size = fundep_size
        self.histograms = None

    @staticmethod
    def register(parser):
        parser.add_argument("--" + DiscreteStats.ID, nargs = 2, metavar = ("max_buckets", "fundep_size"),
                            help = "Find correlations using discrete histograms to count occurences of subtuples. Considers subtuples of size fundep_size, histograms are only retained if they total less than max_buckets distinct classes.")

        #TODO check that fundep_size > 1

    @staticmethod
    def from_parse(params):
        return DiscreteStats(*map(int, params))

    def fit(self, Xs):
        sample = None

        for id, X in enumerate(Xs):
            if id % 10 == 0:
                debug(id, end='\r')

            subtuples = tuple(combinations(tupleops.flatten(X), self.fundep_size))

            if self.histograms == None:
                sample = X
                self.histograms = [Counter() for _ in subtuples]

            for id, subtuple in enumerate(subtuples):
                hist = self.histograms[id]
                if hist != None:
                    hist[subtuple] += 1
                    if len(hist) > self.max_buckets:
                        self.histograms[id] = None

        all_hints = tuple(combinations(tupleops.flatten(tupleops.number(sample)), self.fundep_size))
        self.hints = tuple(hint for hint, hist in zip(all_hints, self.histograms)
                           if hist != None)
        #print(len(all_hints))
        #print(len(self.hints))

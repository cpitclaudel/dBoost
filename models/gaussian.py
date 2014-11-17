from .utils import *
from sklearn import mixture

class Simple:
    def __init__(self):
        self.model = None

    def fit(self, Xs):
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

        self.model = merge(SAVG, SIGMA, id, tuplify)

    @staticmethod
    def test_one(xi, gaussian):
        avg, sigma = gaussian
        return abs(xi - avg) <= 3 * sigma

    def find_discrepancies(self, X, index):
        ret = []
 
        for field_id, (x, m) in enumerate(zip(X, self.model)):
            failed_tests = [test_id for (test_id, (xi, mi))
                                    in enumerate(zip(x, m))
                                    if not Simple.test_one(xi, mi)]
            if len(failed_tests) != 0:
                ret.append((field_id, failed_tests))

        return ret

class Mixture:
    def __init__(self, n_components = 2):
        self.n_components = n_components
        pass

    # TODO: percentile
    def fit(self, Xs):
        Xs = list(Xs)
        flattened = []
        for x in Xs:
            flattened.append([element for tupl in x for element in tupl])
        self.gmm = mixture.GMM(n_components = self.n_components)
        self.gmm.fit(flattened)
        log_prob, responsabilities = self.gmm.score_samples(flattened)
        best_prob = max(log_prob)

        self.keep = [True if lp >= best_prob / 2 else False for lp in log_prob]

    def find_discrepancies(self, X, index):
        #TODO: move score_samples here.
        #TODO: detect which field is wrong using gradient estimation: calculate gradient of prob function at outlier point, find dimension with largest gradient value
        return [] if self.keep[index] else [(0,[])]

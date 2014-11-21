import numbers
from .utils import *
from utils.autoconv import autoconv
from sklearn import mixture

class Simple:
    ID = "gaussian"
    
    def __init__(self, tolerance):
        self.tolerance = tolerance
        self.reset()
        
    def reset(self):
        self.model = None        
        
    @staticmethod
    def register(parser):
        parser.add_argument("--" + Simple.ID, nargs = 1, metavar = "Nstdev")
        
    @staticmethod
    def from_parse(params):
        return Simple(*map(autoconv, params))
        
    def fit(self, Xs):
        S, S2, C = None, None, None

        for (nb, X) in enumerate(Xs):
            report_progress(nb)
            X = filter_abc(X, numbers.Number)
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

    def test_one(self, xi, gaussian):
        avg, sigma = gaussian
        return abs(xi - avg) <= self.tolerance * sigma

    def find_discrepancies(self, X, index):
        ret = []
 
        for field_id, (x, m) in enumerate(zip(X, self.model)):
            failed_tests = [test_id for (test_id, (xi, mi))
                                    in enumerate(zip(x, m))
                                    if not self.test_one(xi, mi)]
            if len(failed_tests) != 0:
                ret.append((field_id, failed_tests))

        return ret

    def more_info(self, field_id, feature_id, feature_name, X, indent = "", pipe = sys.stdout):
        FMT = "{feature_name}: {xi:.2g} falls out of range [{lo:.2f}, {hi:.2f}] = [{mu:.2f} - {t} * {sigma:.2f}, {mu:.2f} + {t} * {sigma:.2f}]\n"
        xi = X[field_id][feature_id]
        t = self.tolerance
        mu, sigma = self.model[field_id][feature_id]
        lo, hi = mu - t * sigma, mu + t * sigma
        pipe.write(indent + FMT.format(**locals()))

class Mixture:
    ID = "mixture"
    
    def __init__(self, n_components):
        self.n_components = n_components

    def reset(self):
        self.gmm = None
        self.keep = None
        
    @staticmethod
    def register(parser):
        parser.add_argument("--" + Mixture.ID, nargs = 1, metavar = "Ncomponents")
        
    @staticmethod
    def from_parse(params):
        return Mixture(*map(autoconv, params))
        
    # TODO: percentile
    def fit(self, Xs):
        Xs = list(map(lambda X: filter_abc(X, numbers.Number), Xs))
        Xs = list(Xs)
        flattened = []
        for x in Xs:
            flattened.append([element for tupl in x for element in tupl])
        self.gmm = mixture.GMM(n_components = self.n_components)
        self.gmm.fit(flattened)
        log_prob, responsabilities = self.gmm.score_samples(flattened)
        best_prob = max(log_prob)

        self.keep = [lp >= best_prob / 2 for lp in log_prob]

    def find_discrepancies(self, X, index):
        #TODO: move score_samples here.
        #TODO: detect which field is wrong using gradient estimation: calculate gradient of prob function at outlier point, find dimension with largest gradient value
        return [] if self.keep[index] else [(0,[])]

    def more_info(self, identifiers, highlighted = None, indent = "", pipe = sys.stdout):
        pass

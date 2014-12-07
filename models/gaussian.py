import numbers
from .utils import *
from utils.autoconv import autoconv
from sklearn import mixture
from numpy import array, percentile

class Simple:
    ID = "gaussian"
    
    def __init__(self, tolerance):
        self.tolerance = tolerance
        self.reset()
        
    def reset(self):
        self.model = None
        
    @staticmethod
    def register(parser):
        parser.add_argument("--" + Simple.ID, nargs = 1, metavar = "n_stdev",
                            help = "Use a gaussian model, reporting values that fall more than " +
                            "n_stdev standard deviations away from the mean. Suggested value: 3.")
        
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
        parser.add_argument("--" + Mixture.ID, nargs = 1, metavar = "n_subpops",
                            help = "Use a gaussian mixture model, reporting values whose probability is " +
                            "below ??, as predicted by a model of the data comprised of n_subpops "+
                            "gaussians. Suggested value: 2.")
        
    @staticmethod
    def from_parse(params):
        return Mixture(*map(autoconv, params))

    def score(self, X):
        X = filter_abc(X, numbers.Number)
        X = flatten(X)
        lp, _ = self.gmm.score_samples([X])
        return lp[0]

    def new_score(self, X):
        X = filter_abc(X, numbers.Number)
        sum_lp = 0
        for i in range(len(X)):
            x = list(X[i])
            lp, _ = self.gmms[i].score_samples([x])
            sum_lp += lp[0]
        return sum_lp
        
    def fit(self, Xs):
        Xs = list(map(lambda X: filter_abc(X, numbers.Number), Xs))
        Xs = [flatten(x) for x in Xs]
        self.gmm = mixture.GMM(n_components = self.n_components)
        self.gmm.fit(Xs)
        #TODO: find non-data dependent value
        log_prob, _ = self.gmm.score_samples(Xs)
        self.cutoff = percentile(array(log_prob),10)

    def new_fit(self, Xs):
        Xs = list(map(lambda X: filter_abc(X, numbers.Number), Xs))
        n = len(Xs[0]) #number of tuples representing correlations
        self.gmms = []

        log_probs = map(lambda _: 0, Xs)
        for correlation in range(0, n):
            to_fit = map(lambda X: list(X[correlation]), Xs)
            self.gmms[correlation] = mixture.GMM(n_components = len(correlation))
            self.fit(to_fit)

            #TODO: find non-data dependent value
            log_prob, _ = self.gmms[correlation].score_samples(to_fit)
            log_probs = [sum(x) for x in zip(log_probs, log_prob)]
        
        self.cutoff = percentile(array(log_prob), 10)
        

    def find_discrepancies(self, X, index):
        log_prob = self.score(X)
        return [] if log_prob > self.cutoff else [(0,[])]

    def more_info(self, identifiers, highlighted = None, indent = "", pipe = sys.stdout):
        pass

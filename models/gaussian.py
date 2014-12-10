import numbers
from utils.tupleops import *
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

        # TODO: Adjust this to use values from the statistical analysis
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

    INFO_FMT = "{feature_name}: {xi:.2g} falls out of range [{lo:.2f}, {hi:.2f}] = [{mu:.2f} - {t} * {sigma:.2f}, {mu:.2f} + {t} * {sigma:.2f}]\n"

    def more_info(self, discrepancy, description, X, indent = "", pipe = sys.stdout):
        assert(len(discrepancy) == 1)

        field_id, feature_id = discrepancy[0]
        feature_name = description[0]

        t = self.tolerance
        xi = X[field_id][feature_id]
        mu, sigma = self.model[field_id][feature_id]
        lo, hi = mu - t * sigma, mu + t * sigma

        pipe.write(indent + Simple.INFO_FMT.format(**locals()))

class Mixture:
    ID = "mixture"
    
    def __init__(self, n_components, cutoff):
        #FIXME: currently unused, using self.cutoffs instead
        self.cutoff = cutoff
        self.n_components = n_components
        
    def reset(self):
        self.gmms    = None
        self.cutoffs = None
        self.cutoff  = None
        self.keep    = None
        
    @staticmethod
    def register(parser): #TODO (Z): fix the doc. Add an extra arg?
        parser.add_argument("--" + Mixture.ID, nargs = 2, metavar = ("n_subpops", "threshold"),
                            help = "Use a gaussian mixture model, reporting values whose probability is " +
                            "below threshold, as predicted by a model of the data comprised of n_subpops "+
                            "gaussians. Suggested value: 2.")
        
    @staticmethod
    def from_parse(params):
        return Mixture(*map(autoconv, params))

    def fit(self, Xs):
        self.gmms = []
        self.cutoffs = []

        correlations = []
        for X in Xs:
            correlations.append(filter_abc(X[0], numbers.Number))

        for c in range(0, len(correlations[0])):
            to_fit = list(map(lambda X: list(X[c]), correlations))
            gmm = mixture.GMM(n_components = self.n_components)
            gmm.fit(to_fit)
            self.gmms.append(gmm)

            lp, _ = self.gmms[c].score_samples(to_fit)
            #FIXME: change cutoff value
            self.cutoffs.append(percentile(array(lp), 90))

    def test_one(self, xi, gmm, cutoff):
        return gmm.score([xi]) <= cutoff

    def find_discrepancies(self, X, index):
        correlations = X[0]
        failed_tests = [] #Contains the index of each correlation that wasn't probable enough

        for i in range(len(correlations)):
            if not self.test_one(correlations[i], self.gmms[i], self.cutoffs[i]):
                failed_tests.append(i)

        #FIXME
        return [] if len(failed_tests) == 0 else [(0, [])] 
        
    def more_info(self, discrepancy, description, X, indent = "", pipe = sys.stdout):
        pass #TODO

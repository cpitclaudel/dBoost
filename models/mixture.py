import numbers
from utils.tupleops import *
from utils.autoconv import autoconv
from sklearn import mixture
from numpy import array, percentile

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
                            "below the threshold percentile, as predicted by a model of the data comprised of n_subpops "+
                            "gaussians. Suggested values: 2, TODO.")
        
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
            self.cutoffs.append(percentile(array(lp), self.cutoff))

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

import numbers
from utils.tupleops import *
from utils.autoconv import autoconv
from sklearn import mixture
from matplotlib import pyplot
from math import erf

class Mixture:
    ID = "mixture"
    
    def __init__(self, n_components, cutoff):
        self.n_components = n_components
        self.cutoff = cutoff
        
    def reset(self):
        self.gmms    = None
        self.cutoff  = None
        self.keep    = None
        
    @staticmethod
    def register(parser): 
        parser.add_argument("--" + Mixture.ID, nargs = 2, metavar = ("n_subpops", "threshold"),
                            help = "Use a gaussian mixture model, reporting values whose probability is " +
                            "below the threshold, as predicted by a model of the data comprised of n_subpops "+
                            "gaussians. Suggested values: 2, 0.3.")
        
    @staticmethod
    def from_parse(params):
        return Mixture(*map(autoconv, params))

    def mahalanobis(self, x, gmm, component):
        mean = gmm.means_[component]
        covar = gmm.covars_[component]
        u = x - mean
        v = u.transpose()

        return sqrt(v.dot(((1 / covar) * u).transpose()))

    def fit(self, Xs):
        self.gmms = []
        self.evt = []
        self.cutoffs = []

        correlations = []
        for X in Xs:
            correlations.append(filter_abc(X[0], numbers.Number))

        for c in range(0, len(correlations[0])):
            to_fit = list(map(lambda X: list(X[c]), correlations))
            gmm = mixture.GMM(n_components = self.n_components)
            gmm.fit(to_fit)
            self.gmms.append(gmm)
            
            # lp, resp = self.gmms[c].score_samples(to_fit)
 
            # ps = [self.test_one(x, c) for x in to_fit]
            # pyplot.hist(ps, bins = 30)
            # pyplot.show()

    def test_one(self, xi, gmm_pos):
        gmm = self.gmms[gmm_pos]
        hx = zip(gmm.weights_, [1-erf(self.mahalanobis(xi, gmm, i))/sqrt(2) for i in range(self.n_components)])
        return sum([w*h for (w,h) in hx])
	
    def find_discrepancies(self, X, index):
        correlations = X[0]
        discrepancies = []
        
        for id, (correlation, gmm_pos, cutoff) in enumerate(zip(correlations, range(len(self.gmms)), range(len(self.gmms)))):
            if self.test_one(correlation, gmm_pos) < self.cutoff:
                discrepancies.append(((0, id),))

        return discrepancies
        
    def more_info(self, discrepancy, description, X, indent = "", pipe = sys.stdout):
        pass #TODO


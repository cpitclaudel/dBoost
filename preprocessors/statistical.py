import numbers
from utils.tupleops import *
from utils.autoconv import autoconv
import math,itertools

# Preprocessor that collects dataset statistics over columns for use by other models.
#   It also detects correlations between columns using the Pearson R coefficient. 
#   If the absolute value of the R value is greater than epsilon, the coordinates of
#   the two columns are added as pairs to hints in the format
#   ( (x-index, x-subcolumn-index), (y-index, y-subcolumn-index))
# Collects the following stats:
#   avg -- average value of the column
#   cnt -- total number of value in the column
#   maxm -- maximum value in the column
#   minm -- minimum value in the column
#   ttl -- sum of values in the column
#   var -- variance
# 

class Pearson:
    ID = "statistical"
    #def __init__(self, proj1, proj2):
    def __init__(self,eps):
        self.eps = eps
        self.reset()

    def reset(self):
      self.hints = [] 
      self.sum = []
      self.avg = []
      self.var = []
      self.cnt = []
      self.maxm = []
      self.minm = []
      self.ttl = []

    @staticmethod
    def register(parser):
        parser.add_argument("--" + Pearson.ID, nargs = 1, metavar = "epsilon",
                            help = "Use a statistical model preprocessor, reporting correlated values " +
                            "with a pearson r value greater than epsilon.") 
 
    @staticmethod
    def from_parse(params):
        return Pearson(*map(float, params))
        
    def fit(self, Xs):
        S,S2,C,SXY = None, None, None,None

        for (nb, X_) in enumerate(Xs):
            # discard first tuple, since this is empty hints tuple
            X_ = X_[1:len(X_)]
            X_ = filter_abc(X_, numbers.Number)
            S, S2, C = zeroif(S, X_), zeroif(S2, X_), zeroif(C, X_)
            S = merge(S, X_, id, plus)
            S2 = merge(S2, X_, sqr, plus)
            C = merge(C, X_, not_null, plus)
            XY_ = () 
            for ((X,Y),(nx,ny)) in zip(itertools.combinations(X_,2),itertools.combinations(range(len(X_)),2)):
              for ((x,y),(nnx,nny)) in zip(itertools.product(zip(*[X]),zip(*[Y])),itertools.product(range(len(X)),range(len(Y)))):
                XY_ = XY_ + ((x[0]*y[0],),)
            SXY = zeroif(SXY,XY_)
            SXY = merge(SXY, XY_, id, plus)

        AVGX = merge(S,C,id,div0)
        AVGSQX = merge(S2,C,id,div0)
        VARX = merge(AVGSQX,AVGX,sqr,minus)

        idx = -1 
        PR = ()
        VARXY = ()

        for ((X,Y),(nx,ny)) in zip(itertools.combinations(X_,2),itertools.combinations(range(len(X_)),2)):
          for (nnx,nny) in itertools.product(range(len(X)),range(len(Y))):
            idx = idx + 1
            VARXY = VARXY + ((SXY[idx][0]/C[nx][nnx] - (AVGX[nx][nnx] * AVGX[ny][nny])),)
            if VARX[nx][nnx] == 0 or VARX[ny][nny] == 0:
              PR = PR + (float('nan'),)
            else:
              PR = PR + ((VARXY[idx] / math.sqrt(VARX[nx][nnx] * VARX[ny][nny])),)
            if not math.isnan(PR[idx]) and math.fabs(PR[idx]) > self.eps:
              self.hints.append(((nx,nnx),(ny,nny)))
            #print(str(nx) + "." + str(nnx) + " " + str(ny) + "." + str(nny) + " " + str(AVGX[nx][nnx]) + " " + str(AVGX[ny][nny]) + " " + str(SXY[idx][0]) + " " + str(PR[idx]))

        self.cnt = C
        self.sum = S 
        self.sum2 = S2 
        self.avg = AVGX 
        self.avg2 = AVGSQX 
        self.var = VARX 
        self.pearson = PR


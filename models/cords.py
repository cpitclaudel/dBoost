import numbers
from utils.tupleops import *
from utils.autoconv import autoconv
import math,itertools
from pprint import pprint

#CORDS: Automatic Discovery of Correlations and Soft Functional Dependencies

class Cords:
    ID = "cords"
    def __init__(self,p):
      self.reset()
      self.p = p
      self.delta = 0.005
      return

    def reset(self):
      self.hints = []
      self.model = None
      return

    @staticmethod
    def register(parser):
        parser.add_argument("--" + Cords.ID, nargs = 1, metavar = "p",
                            help = "Use the CORDS method to find correlated values. p is the maximum worst-case probability of incorrectly rejecting the independence hypothesis. Recommended value: 0.001 ")

    @staticmethod
    def from_parse(params):
        return Cords(*map(float, params))

    def fit(self, Xs,analyzer):
        self.model = analyzer.stats
        # Get stats from statistical preprocessor
        # Collect random sample: skip this for now
        # Contingency tables
        N,Nx,Ny = None, None, None
        for (nb, X_) in enumerate(Xs):
          X_ = filter_abc(X_, numbers.Number)
          # Chi-squared test
          num = 0
          for ((X,Y),(nx,ny)) in zip(itertools.combinations(X_,2),itertools.combinations(range(len(X_)),2)):
            for ((x,y),(nnx,nny)) in zip(itertools.product(zip(*[X]),zip(*[Y])),itertools.product(range(len(X)),range(len(Y)))):
              d1 = analyzer.stats[nx][nnx].cardinality
              d2 = analyzer.stats[ny][nny].cardinality
              if d1 == 1 or d2 == 1 or d1 == float("+inf") or d2 == float("+inf"): continue
              N,Nx,Ny = addlist2d(N,num,d1,d2),addlist(Nx,num,d1),addlist(Ny,num,d2)
              # FIXME: doing mod means that this may generate some buckets with 0 items
              i = hash(x) % d1 #FIXME: hash just returns x for integers
              j = hash(y) % d2
              #print(str(nx) + "." + str(nnx) + " " + str(ny) + "." + str(nny) + ": " + str(d1) + " " + str(d2) + " " + str(i) + " " + str(j))
              N[num][i][j] += 1
              Nx[num][i] += 1
              Ny[num][j] += 1
              num = num+1

        num = 0
        for ((X,Y),(nx,ny)) in zip(itertools.combinations(X_,2),itertools.combinations(range(len(X_)),2)):
          for ((x,y),(nnx,nny)) in zip(itertools.product(zip(*[X]),zip(*[Y])),itertools.product(range(len(X)),range(len(Y)))):
            d1 = analyzer.stats[nx][nnx].cardinality
            d2 = analyzer.stats[ny][nny].cardinality
            if d1 == 1 or d2 == 1 or d1 == float("+inf") or d2 == float("+inf"): continue
            #print(str(nx) + "." + str(nnx) + " " + str(ny) + "." + str(nny) + ": " + str(N[num]))
            #print(str(nx) + "." + str(nnx) + " " + str(ny) + "." + str(nny) + ": " + str(Nx[num]))
            #print(str(nx) + "." + str(nnx) + " " + str(ny) + "." + str(nny) + ": " + str(Ny[num]))
            zeros = sum(N[num][i].count(0) for i in range(d1))
            if zeros > d1 * d2 * 0.5:
              num = num+1
              self.hints.append(((nx,nnx),(ny,nny)))
              continue
            #FIXME: Hackety hack hack
            for i in range(d1):
              if Nx[num][i] == 0: Nx[num][i] = 1
            for j in range(d2):
              if Ny[num][j] == 0: Ny[num][j] = 1
            chi_sqrd = sum( sum( ((N[num][i][j] - (Nx[num][i] * Ny[num][j])) ** 2 ) / (Nx[num][i] * Ny[num][j]) for i in range(d1)) for j in range(d2))
            d = min(d1,d2)
            v = (d1 - 1) * (d2 - 1)
            n = (math.sqrt(-16 * v * math.log(self.p * math.sqrt(2*math.pi))) - 8 * math.log(self.p * math.sqrt(2*math.pi)) ) / (1.69 * self.delta * (d - 1) * pow(v,-0.071))
            lda = n * (d - 1) * self.delta
            t = 1 / (0.5 * ( 1+ math.erf( ((1 - self.p) - (v + lda)) / (math.sqrt( 2*v + 4*lda)) )))
            #t = norm.ppf(norm.cdf( ((1 - self.p) - (v + lda)) / (math.sqrt( 2*v + 4*lda)) ))
            print(str(nx) + "." + str(nnx) + " " + str(ny) + "." + str(nny) + ": ")
            print(chi_sqrd)
            print(str(t) + " "+ str(d) +" "+  str(v) +" "+  str(n))
            if chi_sqrd > t:
              self.hints.append(((nx,nnx),(ny,nny)))
            num = num+1
        print(self.hints)

    def find_discrepancies(self, X, index):
      ret = []
      return ret

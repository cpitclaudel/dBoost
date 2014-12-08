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
        
    def new_row(self,n,n2):
        self.cnt = [[0 for j in range(n)] for i in range(n2)]
        self.avg = [[0 for j in range(n)] for i in range(n2)]
        self.var = [[0 for j in range(n)] for i in range(n2)]
        self.sum2 = [[0 for j in range(n)] for i in range(n2)]
        self.model = [[0 for j in range(n)] for i in range(n2)]
        self.maxm = [[0 for j in range(n)] for i in range(n2)]
        self.minm = [[0 for j in range(n)] for i in range(n2)]
        self.hints_ = [[0 for j in range(n)] for i in range(n2)]

     #Pearson Product Moment Coefficient Correlation
    def ppmcc(self, X, Y,nx,nnx,ny,nny):
        n = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        sum_xy = 0
        minm = float('nan')
        maxm = float('nan')
        minmy = float('nan')
        maxmy = float('nan')
        for x_,y_ in zip(X,Y):
            #x, y = self.proj1(X), self.proj2(X)
            try:
              x = int(x_)
              y = int(y_)
            except:
              return 0 

            n += 1
            sum_xy += x * y

            sum_x += x
            sum_x2 += x * x
            if self.cnt[nx][nnx] == 0:
              #sum_x += x
              #sum_x2 += x * x
              if math.isnan(maxm) or x > maxm:
                maxm = x
              if math.isnan(minm) or x < minm:
                minm = x

            sum_y += y
            sum_y2 += y * y
            if self.cnt[ny][nny] == 0:
              #sum_y += y
              #sum_y2 += y * y
              if math.isnan(maxmy) or y > maxmy:
                maxm = x
              if math.isnan(minmy) or y < minmy:
                minm = x

        if self.cnt[nx][nnx] == 0:
          x̄ = sum_x / n
          x̄2̄ = sum_x2 / n
          σ2x = x̄2̄ - (x̄ ** 2)
          self.cnt[nx][nnx] = n
          self.sum2[nx][nnx] = x̄2̄
          self.avg[nx][nnx] = x̄
          self.var[nx][nnx] = σ2x
          self.maxm[nx][nnx] = maxm
          self.minm[nx][nnx] = minm
        else:
          x̄ = self.avg[nx][nnx]
          σ2x = self.var[nx][nnx]

        x̄ = sum_x / n
        x̄2̄ = sum_x2 / n
        σ2x = x̄2̄ - (x̄ ** 2)

        if self.cnt[ny][nny] == 0:
          ȳ = sum_y / n
          ȳ2̄ = sum_y2 / n
          σ2y = ȳ2̄ - (ȳ ** 2)
          self.cnt[ny][nny] = n
          self.sum2[ny][nny] = ȳ2̄
          self.avg[ny][nny] = ȳ
          self.var[ny][nny] = σ2y
          self.maxm[ny][nny] = maxmy
          self.minm[ny][nny] = minmy
        else:
          ȳ = self.avg[ny][nny]
          σ2y = self.var[ny][nny]

        ȳ = sum_y / n
        ȳ2̄ = sum_y2 / n
        σ2y = ȳ2̄ - (ȳ ** 2)

        x̄ȳ = sum_xy / n
        σ2xy = x̄ȳ - (x̄ * ȳ)

        if σ2x == 0 or σ2y == 0:
          pearson = float('nan') 
        else:
          #print(X,Y)
          pearson = σ2xy / math.sqrt(σ2x * σ2y)
        #print(n,sum_x,sum_y,sum_x2,sum_y2,sum_xy)
        if not math.isnan(pearson) and math.fabs(pearson) > self.eps:
          self.hints.append(((nx,nnx),(ny,nny)))
          #print(str(nx) + "." + str(nnx) + " " + str(ny) + "." + str(nny) + " " + str(pearson))

        return pearson

    def fit(self, Xs):
      Xs_ = list(Xs)
      #print(len(Xs_))# Number of columns
      #print(len(Xs_[0])) # Number of values in each col
      #print(len(Xs_[0][0])) # Number of sub-columns
      #print(max([len(Xs_[0][i]) for i in range(len(Xs_))]))
      self.new_row(max([len(Xs_[i][0]) for i in range(len(Xs_))]),len(Xs_))
      #print(Xs_)
      for ((X,Y),(nx,ny)) in zip(itertools.combinations(Xs_,2),itertools.combinations(range(len(Xs_)),2)):
        #print(X[0][len(X[0])-1])
        #print(Y[0][len(Y[0])-1])
        for ((x,y),(nnx,nny)) in zip(itertools.product(zip(*X),zip(*Y)),itertools.product(range(len(X[0])),range(len(Y[0])))):
          pearson = self.ppmcc(x,y,nx,nnx,ny,nny)

    #print(self.hints)


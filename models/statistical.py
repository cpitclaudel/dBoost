import math,itertools

class Pearson:
    #def __init__(self, proj1, proj2):
    def __init__(self,eps):
        self.model = [] 
        self.eps = eps

        #self.proj1 = proj1
        #self.proj2 = proj2

     #Pearson Product Moment Coefficient Correlation
    def ppmcc(self, X, Y):
        n = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        sum_xy = 0
        for x,y in zip(X,Y):
            #x, y = self.proj1(X), self.proj2(X)

            n += 1
            sum_x += x
            sum_y += y
            
            sum_x2 += x * x
            sum_y2 += y * y
            sum_xy += x * y

        x̄ = sum_x / n
        ȳ = sum_y / n
        
        x̄2̄ = sum_x2 / n
        ȳ2̄ = sum_y2 / n
        x̄ȳ = sum_xy / n
        
        σ2x = x̄2̄ - (x̄ ** 2)
        σ2y = ȳ2̄ - (ȳ ** 2)
        σ2xy = x̄ȳ - (x̄ * ȳ)
        
        if σ2x == 0 or σ2y == 0:
          self.pearson = float('nan') 
        else:
          print(X,Y)
          self.pearson = σ2xy / math.sqrt(σ2x * σ2y)
        return self.pearson

    def fit(self, Xs,Ys):
      len1 = 0;
      for X,Y in itertools.product(list(Xs),list(Ys)):
        print(X)
        print(Y)
        len1 = 0
        for x,y in itertools.product(zip(*X),zip(*Y)):
          self.model.append(self.ppmcc(x,y))
          len1 = len1+1
      self.model =[self.model[i:i+len1] for i in range(0, len(self.model), len1)] 
      print(len1)
      print(self.model)


    def find_discrepancies(self, X,index):
      ret = []
      k = list(enumerate(X))

      idx0 = -1 
      idx1 = -1 
      for field_idx,x in k:
        for field_idy, y in k:
          idx0 = idx0+1
          idx1 = -1
          if field_idx == field_idy: continue
          for x1,y1 in itertools.product(x,y):
            idx1 = idx1+1
            if math.isnan(self.model[idx0][idx1]): continue
            #TODO: How to determine whether these 2 values are within eps of the correlation coefficient?
          
        
      return ret

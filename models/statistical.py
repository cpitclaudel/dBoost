import math

class Pearson:
    def __init__(self, proj1, proj2):
        self.n = 0
        self.sum_x = 0
        self.sum_y = 0
        self.sum_x2 = 0
        self.sum_y2 = 0
        self.sum_xy = 0

        self.proj1 = proj1
        self.proj2 = proj2
        
    def fit(self, Xs):
        for X in Xs:
            x, y = self.proj1(X), self.proj2(X)

            self.n += 1
            self.sum_x += x
            self.sum_y += y
            
            self.sum_x2 += x * x
            self.sum_y2 += y * y
            self.sum_xy += x * y

        self.x̄ = self.sum_x / self.n
        self.ȳ = self.sum_y / self.n
        
        self.x̄2̄ = self.sum_x2 / self.n
        self.ȳ2̄ = self.sum_y2 / self.n
        self.x̄ȳ = self.sum_xy / self.n
        
        self.σ2x = self.x̄2̄ - (self.x̄ ** 2)
        self.σ2y = self.ȳ2̄ - (self.ȳ ** 2)
        self.σ2xy = self.x̄ȳ - (self.x̄ * self.ȳ)
        
        self.pearson = self.σ2xy / math.sqrt(self.σ2x * self.σ2y)

    def find_discrepancies(self, X, index):
        return [] # TODO?

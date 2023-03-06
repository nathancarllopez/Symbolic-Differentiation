import math

class Exponential(DifferentiableFunction):
    def __init__(self, coeff, base):
        assert base > 0
        self.coeff = coeff
        self.base = base
        DifferentiableFunction.__init__(self, lambda x: coeff * math.pow(base, x))

    def __str__(self):
        if self.base == 1:
            return str(self.coeff)
        if self.coeff == 1:
            return str(self.base) + '^x'
        return str(self.coeff) + '*' + str(self.base) + '^x'
    
    def derivative(self):
        return Exponential(round(self.coeff * math.log(self.base), 2), self.base)
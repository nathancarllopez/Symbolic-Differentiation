import math
from structure import AlgebraicStructure
from main import DifferentiableFunction

class Exponential(DifferentiableFunction):
    def __init__(self, argument, coeff, base):
        assert base > 0, "Base needs to be positive"
        self.coeff = coeff
        self.base = base
        structure = AlgebraicStructure(self, [])
        DifferentiableFunction.__init__(
            self, 
            argument, 
            lambda x: coeff * math.pow(base, x),
            structure
            )

    def __str__(self):
        if self.base == 1:
            return str(self.coeff)
        if self.coeff == 1:
            return str(self.base) + '^' + str(self.argument)
        return str(self.coeff) + '*' + str(self.base) + '^' + str(self.argument)
    
    def derivative(self):
        return Exponential(self.argument, round(self.coeff * math.log(self.base), 2), self.base)

f = Exponential('x', 3, 5)
print(f)
print(f.structure)
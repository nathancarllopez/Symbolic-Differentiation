import math
import random

class DifferentiableFunction():
    def __init__(self, rule):
        self.rule = rule

    def evaluate(self, input):
        return self.rule(input)
    
    def __add__(self, other):
        return DifferentiableFunction(lambda x: self.rule(x) + other.rule(x))
    
class Monomial(DifferentiableFunction):
    def base_rule(x, coeff, power):
        terms = (x for i in range(power))
        return coeff * math.prod(terms)
    
    def __init__(self, coeff, power):
        self.coeff = coeff
        self.power = power
        rule = lambda x: Monomial.base_rule(x, coeff, power)
        DifferentiableFunction.__init__(self, rule)

    def derivative(self):
        return Monomial(self.coeff * self.power, self.power - 1)
    
    def __str__(self):
        if self.power > 1:
            if self.coeff == 1:
                return 'x^' + str(self.power)
            elif self.coeff == -1:
                return '-x^' + str(self.power)
            elif self.coeff == 0:
                return str(self.coeff)
            else:
                return str(self.coeff) + 'x^' + str(self.power)
        elif self.power == 1:
            if self.coeff == 1:
                return 'x'
            elif self.coeff == -1:
                return '-x'
            elif self.coeff == 0:
                return str(self.coeff)
            else:
                return str(self.coeff) + 'x'
        else:
            return str(self.coeff)
    
class Polynomial(DifferentiableFunction):
    def base_rule(x, coeffs):
        top_power = len(coeffs)
        terms = []
        for i in range(top_power):
            terms.append(Monomial.base_rule(x, coeffs[i], top_power - 1 - i))
        return sum(terms)
    
    def __init__(self, coeffs):
        self.coeffs = coeffs
        rule = lambda x: Polynomial.base_rule(x, coeffs)
        DifferentiableFunction.__init__(self, rule)

    def __str__(self):
        top_power = len(self.coeffs)
        terms = []
        for i in range(top_power):
            if self.coeffs[i] == 0:
                continue
            else:
                terms.append(str(Monomial(self.coeffs[i], top_power - 1 - i)))
        result = terms[0]
        for i in range(1, len(terms)):
            next_term = terms[i]
            if next_term[0] == '-':
                new_term = next_term[1:]
                result += ' - ' + new_term
            else:
                result += ' + ' + next_term
        return result
    
    def derivative(self):
        pass
    
for k in range(5):
    coeffs = [random.randint(-5,5) for k in range(4)]
    print(Polynomial(coeffs))
import math
import random

class DifferentiableFunction():
    def __init__(self, rule):
        self.rule = rule

    def evaluate(self, input):
        return self.rule(input)
    
    def __add__(self, other):
        return DifferentiableFunction(lambda x: self.rule(x) + other.rule(x))
    
    def __sub__(self, other):
        return DifferentiableFunction(lambda x: self.rule(x) - other.rule(x))
    
    def __mul__(self, other):
        return DifferentiableFunction(lambda x: self.rule(x) * other.rule(x))
    
    def __truediv__(self, other):
        return DifferentiableFunction(lambda x: self.rule(x) / other.rule(x))
    
class Polynomial(DifferentiableFunction):
    def base_rule(x, coeffs):
        num_of_terms = len(coeffs)
        terms = (coeffs[i] * x ** (num_of_terms - 1 - i) for i in range(num_of_terms))
        return sum(terms)

    def __init__(self, coeffs):
        self.coeffs = coeffs
        DifferentiableFunction.__init__(self, lambda x: Polynomial.base_rule(x, coeffs))

    def __str__(self):
        result = ''
        for position, coeff in enumerate(self.coeffs):
            power = len(self.coeffs) - 1 - position
            if coeff == 0:
                continue
            if power > 1:
                if result == '':
                    if coeff == 1:
                        first_term = 'x^' + str(power)
                        result = first_term
                    elif coeff == -1:
                        first_term = '-x^' + str(power)
                        result = first_term
                    else:
                        first_term = str(coeff) + 'x^' + str(power)
                        result = first_term
                else:
                    if coeff > 0:
                        result += ' + '
                        if coeff == 1:
                            result += 'x^' + str(power)
                        else:
                            result += str(coeff) + 'x^' + str(power)
                    else:
                        result += ' - '
                        if coeff == -1:
                            result += 'x^' + str(power)
                        else:
                            coeff = -coeff
                            result += str(coeff) + 'x^' + str(power)
            elif power == 1:
                if result == '':
                    if coeff == 1:
                        first_term = 'x'
                        result = first_term
                    elif coeff == -1:
                        first_term = '-x'
                        result = first_term
                    else:
                        first_term = str(coeff) + 'x'
                        result = first_term
                else:
                    if coeff > 0:
                        result += ' + '
                        if coeff == 1:
                            result += 'x'
                        else:
                            result += str(coeff) + 'x'
                    else:
                        result += ' - '
                        if coeff == -1:
                            result += 'x'
                        else:
                            coeff = -coeff
                            result += str(coeff) + 'x'
            else:
                if result == '':
                    result = str(coeff)
                else:
                    if coeff > 0:
                        result += ' + ' + str(coeff)
                    else:
                        coeff = -coeff
                        result += ' - ' + str(coeff)
        return result

    def derivative(self):
        deriv_coeffs = []
        for position, coeff in enumerate(self.coeffs):
            power = len(self.coeffs) - 1 - position
            deriv_coeffs.append(power * coeff)
        deriv_coeffs.pop()
        return Polynomial(deriv_coeffs)

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

f = Exponential(1, .5)
print(f)
print(f.derivative())
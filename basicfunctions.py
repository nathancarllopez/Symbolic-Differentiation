import math
import random
from structure import AlgebraicStructure

class DifferentiableFunction():
    def __init__(self, argument, rule, structure):
        self.argument = argument
        self.rule = rule
        self.structure = structure
    
    def __add__(self, other):
        assert self.argument == other.argument, "Arguments need to match"
        s_rule = lambda x: self.rule(x) + other.rule(x)
        s_structure = self.structre + other.structure
        s = DifferentiableFunction(self.argument, s_rule, s_structure)
        return s
    
    def differentiate(self):
        result = DifferentiableFunction(lambda x: x)

        # Pseudocode:
        # 1) Start at the root 'R' of the structure tree
        # 2) If the child node is 'L', then take the proper derivative of
        #   the rule attached to the edge (R, L), and return the result
        # 3) Otherwise, the child node is an operation, e.g., +, -, *, /, comp
        # 4) Apply the appropriate calculus derivative rule according to
        #   whatever operation is given, and combine the rules labeling
        #   the edges
        return result
    
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
    
class Polynomial(DifferentiableFunction):

    def base_rule(x, coeffs):
        num_of_terms = len(coeffs)
        terms = (coeffs[i] * x ** (num_of_terms - 1 - i) for i in range(num_of_terms))
        return sum(terms)

    def __init__(self, argument, coeffs):
        self.coeffs = coeffs
        structure = AlgebraicStructure(self, [])
        DifferentiableFunction.__init__(
            self,
            argument,
            lambda x: Polynomial.base_rule(x, coeffs),
            structure
            )

    def __str__(self):
        result = ''
        for position, coeff in enumerate(self.coeffs):
            power = len(self.coeffs) - 1 - position
            if coeff == 0:
                continue
            if power > 1:
                if result == '':
                    if coeff == 1:
                        first_term = str(self.argument) + '^' + str(power)
                        result = first_term
                    elif coeff == -1:
                        first_term = '-' + str(self.argument) + '^' + str(power)
                        result = first_term
                    else:
                        first_term = str(coeff) + str(self.argument) + '^' + str(power)
                        result = first_term
                else:
                    if coeff > 0:
                        result += ' + '
                        if coeff == 1:
                            result += str(self.argument) + '^' + str(power)
                        else:
                            result += str(coeff) + str(self.argument) + '^' + str(power)
                    else:
                        result += ' - '
                        if coeff == -1:
                            result += str(self.argument) + '^' + str(power)
                        else:
                            coeff = -coeff
                            result += str(coeff) + str(self.argument) + '^' + str(power)
            elif power == 1:
                if result == '':
                    if coeff == 1:
                        first_term = str(self.argument)
                        result = first_term
                    elif coeff == -1:
                        first_term = '-' + str(self.argument)
                        result = first_term
                    else:
                        first_term = str(coeff) + str(self.argument)
                        result = first_term
                else:
                    if coeff > 0:
                        result += ' + '
                        if coeff == 1:
                            result += str(self.argument)
                        else:
                            result += str(coeff) + str(self.argument)
                    else:
                        result += ' - '
                        if coeff == -1:
                            result += str(self.argument)
                        else:
                            coeff = -coeff
                            result += str(coeff) + str(self.argument)
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
    

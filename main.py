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
    
class Monomial1(DifferentiableFunction):
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
    
class Polynomial1(DifferentiableFunction):
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
        top_power = len(coeffs)
        self.terms = []
        for i in range(top_power):
            self.terms.append(Monomial(coeffs[i], top_power - 1 - i))

    def __str__(self):
        terms_as_strings = list(map(str, self.terms))
        first_term = ''
        while first_term == '':
            lead = terms_as_strings.pop(0)
            if lead != '0':
                first_term = lead
        result = first_term
        for i in range(len(terms_as_strings)):
            next_term = terms_as_strings[i]
            if next_term == '0':
                continue
            if next_term[0] == '-':
                new_term = next_term[1:]
                result += ' - ' + new_term
            else:
                result += ' + ' + next_term
        return result
    
    def derivative(self):
        pass

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


class Monomial(Polynomial):
    pass

for j in range(5):
    f = Polynomial([random.randint(-3,3) for k in range(7)])
    print("function:", f)
    print("derivative:", f.derivative())
    print()
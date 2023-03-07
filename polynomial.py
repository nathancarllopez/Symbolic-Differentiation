from main import DifferentiableFunction
from structure import AlgebraicStructure

class Polynomial(DifferentiableFunction):
    def base_rule(x, coeffs):
        num_of_terms = len(coeffs)
        terms = (coeffs[i] * x ** (num_of_terms - 1 - i) for i in range(num_of_terms))
        return sum(terms)

    def __init__(self, argument, coeffs):
        self.coeffs = coeffs
        DifferentiableFunction.__init__(self, argument, lambda x: Polynomial.base_rule(x, coeffs))

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

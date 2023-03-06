from main import DifferentiableFunction

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
import math

class DifferentiableFunction():
    def __init__(self, argument, rule, structure):
        '''
        A single-variable function that is differentiable.
        For example, f(x) = 3x + 2^x

        Parameters 
        ----------
        argument (string or DifferentiableFunction)
            The input of the function
            For example, the 'x' in f above
        rule (function)
            The way that the argument is processed to produce an output
            For example, the 3x + 2^x in f above
        structure (AlgebraicStructure)
            A stack that records the way a differentiable function is
            comprised of elementary functions (subclasses) and function
            operations: +, -, *, /, and compose
        '''
        self.argument = argument
        self.rule = rule
        self.structure = structure

    def __str__(self):
        stack = self.structure.copy()
        top = stack.pop()
        if top in ['+', '-', '*', '/', 'compose']:
            first = stack.pop()
            second = stack.pop()
            if top == '+':
                return DifferentiableFunction.__str__(first) + ' ' + top + ' ' + DifferentiableFunction.__str__(second)
            if top == '-':
                return DifferentiableFunction.__str__(first) + ' ' + top + ' (' + DifferentiableFunction.__str__(second) + ')'
            if top == '*':
                return '(' + DifferentiableFunction.__str__(first) + ')(' + DifferentiableFunction.__str__(second) + ')'
            if top == '/':
                return '(' + DifferentiableFunction.__str__(first) + ') / (' + DifferentiableFunction.__str__(second) + ')'
            if top == 'compose':
                argument = DifferentiableFunction.__str__(second)
                if type(first) is DifferentiableFunction:
                    composition = DifferentiableFunction(
                        argument,
                        lambda x: first.rule(second.rule(x)),
                        second.structure
                    )
                    return DifferentiableFunction.__str__(composition)
                else:
                    composition = type(first).compose(first, argument)
                    return type(first).__str__(composition)
        else:
            return type(top).__str__(top)

    ##########################
    ## Algebraic Operations ##
    ##########################

    def __add__(self, other):
        s_rule = lambda x: self.rule(x) + other.rule(x)
        s_structure = [other, self, '+']
        s = DifferentiableFunction(self.argument, s_rule, s_structure)
        return s
    
    def __mul__(self, other):
        m_rule = lambda x: self.rule(x) * other.rule(x)
        m_structure = [other, self, '*']
        m = DifferentiableFunction(self.argument, m_rule, m_structure)
        return m
    
    def __sub__(self, other):
        d_rule = lambda x: self.rule(x) - other.rule(x)
        d_structure = [other, self, '-']
        d = DifferentiableFunction(self.argument, d_rule, d_structure)
        return d
    
    def __truediv__(self, other):
        f_rule = lambda x: self.rule(x) / other.rule(x)
        f_structure = [other, self, '/']
        f = DifferentiableFunction(self.argument, f_rule, f_structure)
        return f
    
    def compose(self, other):
        c_rule = lambda x: self.rule(other.rule(x))
        c_structure = [other, self, 'compose']
        c = DifferentiableFunction(str(other), c_rule, c_structure)
        return c
    
    ####################
    ## Calculus Rules ##
    ####################

    def productRule(self, other):
        first_term = type(self).derivative(self) * other
        second_term = self * type(other).derivative(other)
        return first_term + second_term

    def quotientRule(self, other):
        first_num = type(self).derivative(self) * other
        second_num = self * type(other).derivative(other)
        num = first_num - second_num
        denom = other * other
        return num / denom

    def chainRule(self, other):
        deriv_outside = type(self).derivative(self)
        first_term = DifferentiableFunction.compose(deriv_outside, other)
        second_term = type(other).derivative(other)
        return first_term * second_term

    def applyDerRule(self, other, operation):
        if operation == '+':
            return type(self).derivative(self) + type(other).derivative(other)
        if operation == '-':
            return type(self).derivative(self) - type(other).derivative(other)
        rule_dict = {
            '*': DifferentiableFunction.productRule,
            '/': DifferentiableFunction.quotientRule,
            'compose': DifferentiableFunction.chainRule
        }
        return rule_dict[operation](self, other)
    
    def differentiate(self):
        pass


class Polynomial(DifferentiableFunction):
    def base_rule(x, coeffs):
        num_of_terms = len(coeffs)
        terms = (coeffs[i] * x ** (num_of_terms - 1 - i) for i in range(num_of_terms))
        return sum(terms)

    def __init__(self, coeffs, argument='x'):
        self.coeffs = coeffs
        structure = [self]
        DifferentiableFunction.__init__(
            self,
            argument,
            lambda x: Polynomial.base_rule(x, coeffs),
            structure
            )
        
    def compose(self, argument):
        return Polynomial(self.coeffs, argument)

    def __str__(self):
        if len(self.argument) > 1:
            self.argument = '(' + self.argument + ')'
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
        return Polynomial(self.argument, deriv_coeffs)


class Exponential(DifferentiableFunction):
    def __init__(self, coeff, base, argument='x'):
        assert base > 0, "Base needs to be positive"
        self.coeff = coeff
        self.base = base
        structure = [self]
        DifferentiableFunction.__init__(
            self, 
            argument, 
            lambda x: coeff * math.pow(base, x),
            structure
            )
        
    def compose(self, argument):
        return Exponential(self.coeff, self.base, argument)

    def __str__(self):
        if len(self.argument) > 1:
            self.argument = '(' + self.argument + ')'
        if self.base == 1:
            return str(self.coeff)
        if self.coeff == 1:
            return str(self.base) + '^' + str(self.argument)
        return str(self.coeff) + '*' + str(self.base) + '^' + str(self.argument)
    
    def derivative(self):
        return Exponential(self.argument, round(self.coeff * math.log(self.base), 2), self.base)
        

class Trigonometric(DifferentiableFunction):
    def __init__(self, coeff, flavor, argument='x'):
        '''
        flavor parameter determines sine or cosine:
        'c' -> cosine
        's' -> sine
        '''
        self.coeff = coeff
        self.flavor = flavor
        if flavor == 's':
            rule = lambda x: coeff * math.sin(x)
        elif flavor == 'c':
            rule = lambda x: coeff * math.cos(x)
        else:
            raise ValueError
        structure = [self]
        DifferentiableFunction.__init__(
            self,
            argument,
            rule,
            structure
        )

    def compose(self, argument):
        return Trigonometric(self.coeff, self.flavor, argument)

    def __str__(self):
        if len(self.argument) > 1:
            self.argument = '(' + self.argument + ')'
        if self.flavor == 's':
            if self.coeff == 1:
                return 'sin(' + str(self.argument) + ')'
            return str(self.coeff) + '*sin(' + str(self.argument) + ')'
        if self.coeff == 1:
            return 'cos(' + str(self.argument) + ')'
        return str(self.coeff) + '*cos(' + str(self.argument) + ')'

    def derivative(self):
        if self.flavor == 's':
            return Trigonometric(self.argument, self.coeff, 'c')
        return Trigonometric(self.argument, -self.coeff, 's')
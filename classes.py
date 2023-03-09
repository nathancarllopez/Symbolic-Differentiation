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
            A tree that describes that way a function is comprised of other functions
            For example, f above combines 3x and 2^x with addition
            See the docstring for AlgebraicStructure for more info
        '''
        self.argument = argument
        self.rule = rule
        self.structure = structure

    def __str__(self):
        operation = self.structure.root
        if operation in ['+', '-', '*', '/', 'compose']:
            self_child, other_child = self.structure.self_child, self.structure.other_child
            if type(self_child) is AlgebraicStructure:
                if type(other_child) is AlgebraicStructure:
                    # both children are structures
                    self_child_function = AlgebraicStructure.unpack(self_child)
                    other_child_function = AlgebraicStructure.unpack(other_child)
                    if operation == '+':
                        return DifferentiableFunction.__str__(self_child_function) + ' + ' + DifferentiableFunction.__str__(other_child_function)
                    if operation == '-':
                        return DifferentiableFunction.__str__(self_child_function) + ' - ' + DifferentiableFunction.__str__(other_child_function)
                    if operation == '*':
                        return '(' + DifferentiableFunction.__str__(self_child_function) + ')(' + DifferentiableFunction.__str__(other_child_function) + ')'
                    if operation == '/':
                        return '(' + DifferentiableFunction.__str__(self_child_function) + ') / (' + DifferentiableFunction.__str__(other_child_function) + ')'
                    if operation == 'compose':
                        return "I'm not sure about this one yet"
                else:
                    # self is a structure, other is a function
                    self_child_function = AlgebraicStructure.unpack(self_child)
                    if operation == '+':
                        return DifferentiableFunction.__str__(self_child_function) + ' + ' + DifferentiableFunction.__str__(other_child)
                    if operation == '-':
                        return DifferentiableFunction.__str__(self_child_function) + ' - ' + DifferentiableFunction.__str__(other_child)
                    if operation == '*':
                        return '(' + DifferentiableFunction.__str__(self_child_function) + ')(' + DifferentiableFunction.__str__(other_child) + ')'
                    if operation == '/':
                        return '(' + DifferentiableFunction.__str__(self_child_function) + ') / (' + DifferentiableFunction.__str__(other_child) + ')'
                    if operation == 'compose':
                        return "I'm not sure about this one yet"
            else:
                if type(other_child) is AlgebraicStructure:
                    # self is a function, other is a structure
                    other_child_function = AlgebraicStructure.unpack(other_child)
                    if operation == '+':
                        return DifferentiableFunction.__str__(self_child) + ' + ' + DifferentiableFunction.__str__(other_child_function)
                    if operation == '-':
                        return DifferentiableFunction.__str__(self_child) + ' - ' + DifferentiableFunction.__str__(other_child_function)
                    if operation == '*':
                        return '(' + DifferentiableFunction.__str__(self_child) + ')(' + DifferentiableFunction.__str__(other_child_function) + ')'
                    if operation == '/':
                        return '(' + DifferentiableFunction.__str__(self_child) + ') / (' + DifferentiableFunction.__str__(other_child_function) + ')'
                    if operation == 'compose':
                        return "I'm not sure about this one yet"
                else:
                    # both children are functions
                    if operation == '+':
                        return DifferentiableFunction.__str__(self_child) + ' + ' + DifferentiableFunction.__str__(other_child)
                    if operation == '-':
                        return DifferentiableFunction.__str__(self_child) + ' - ' + DifferentiableFunction.__str__(other_child)
                    if operation == '*':
                        return '(' + DifferentiableFunction.__str__(self_child) + ')(' + DifferentiableFunction.__str__(other_child) + ')'
                    if operation == '/':
                        return '(' + DifferentiableFunction.__str__(self_child) + ') / (' + DifferentiableFunction.__str__(other_child) + ')'
                    if operation == 'compose':
                        return "I'm not sure about this one yet"
        else:
            return str(operation)

    ##########################
    ## Algebraic Operations ##
    ##########################

    def __add__(self, other):
        assert self.argument == other.argument, "Arguments need to match"
        s_rule = lambda x: self.rule(x) + other.rule(x)
        s_structure = self.structure + other.structure
        s = DifferentiableFunction(self.argument, s_rule, s_structure)
        return s
    
    def __mul__(self, other):
        assert self.argument == other.argument, "Arguments need to match"
        m_rule = lambda x: self.rule(x) * other.rule(x)
        m_structure = self.structure * other.structure
        m = DifferentiableFunction(self.argument, m_rule, m_structure)
        return m
    
    def __sub__(self, other):
        assert self.argument == other.argument, "Arguments need to match"
        d_rule = lambda x: self.rule(x) - other.rule(x)
        d_structure = self.structure - other.structure
        d = DifferentiableFunction(self.argument, d_rule, d_structure)
        return d
    
    def __truediv__(self, other):
        assert self.argument == other.argument, "Arguments need to match"
        f_rule = lambda x: self.rule(x) / other.rule(x)
        f_structure = self.structure / other.structure
        f = DifferentiableFunction(self.argument, f_rule, f_structure)
        return f
    
    def compose(self, other):
        c_rule = lambda x: self.rule(other.rule(x))
        c_structure = AlgebraicStructure.compose(self.structure, other.structure)
        c = DifferentiableFunction(other.argument, c_rule, c_structure)
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
        return AlgebraicStructure.differentiate(self.structure)
        # if tree.root in ['+', '*', '-', '/', 'compose']:
        #     self_child, other_child = AlgebraicStructure.getChildren(tree)


        #     ## What happens if the children are also trees? ##
        #     if type(self_child) is AlgebraicStructure:
        #         self_child = AlgebraicStructure.genFunction(self_child)
        #     if type(other_child) is AlgebraicStructure:
        #         other_child = AlgebraicStructure.genFunction(other_child)
        #     ## ##

        #     if tree.root == '+':
        #         return DifferentiableFunction.differentiate(self_child) + DifferentiableFunction.differentiate(other_child)
        #     if tree.root == '-':
        #         return DifferentiableFunction.differentiate(self_child) - DifferentiableFunction.differentiate(other_child)
        #     if tree.root == '*':
        #         return DifferentiableFunction.productRule(self_child, other_child)
        #     if tree.root == '/':
        #         return DifferentiableFunction.quotientRule(self_child, other_child)
        #     if tree.root == 'compose':
        #         return DifferentiableFunction.chainRule(self_child, other_child)
        # else:
        #     root_type = type(tree.root)
        #     return root_type.derivative(tree.root)


class AlgebraicStructure():
    def __init__(self, root, self_child=None, other_child=None):
        # Initialize attributes
        self.root = root
        self.self_child = self_child
        self.other_child = other_child

        # Add edges
        self.edges = []
        if self_child is not None:
            self.edges.append((root, self_child))
        if other_child is not None:
            self.edges.append((root, other_child))

        # Initialize weights dictionary
        self.weights = {edge: None for edge in self.edges}

    def __str__(self):
        if self.root in ['+', '*', '-', '/', 'compose']:
            root_str = 'The root of the graph is '
            root_str += self.root + '.'
            stem_str = 'The first stem is ' + type(self.self_child).__str__(self.self_child) + '.\n'
            stem_str += 'The second stem is ' + type(self.other_child).__str__(self.other_child) + '.'
            return root_str + '\n' + stem_str
        else:
            root_str = type(self.root).__str__(self.root)
            return root_str

    def unpack(self):
        '''
        Returns a differentiable function f with the property
        that f.structure = self
        '''
        operation = self.root
        if operation in ['+', '*', '-', '/', 'compose']:
            self_child, other_child = self.self_child, self.other_child
            if self_child is AlgebraicStructure:
                if other_child is AlgebraicStructure:
                    # both children are structures
                    if operation == '+':
                        return AlgebraicStructure.unpack(self_child) + AlgebraicStructure.unpack(other_child)
                    if operation == '-':
                        return AlgebraicStructure.unpack(self_child) - AlgebraicStructure.unpack(other_child)
                    if operation == '*':
                        return AlgebraicStructure.unpack(self_child) * AlgebraicStructure.unpack(other_child)
                    if operation == '/':
                        return AlgebraicStructure.unpack(self_child) / AlgebraicStructure.unpack(other_child)
                    if operation == 'compose':
                        return DifferentiableFunction.compose(AlgebraicStructure.unpack(self_child), AlgebraicStructure.unpack(other_child))
                else:
                    # self is a structure, other is a function
                    if operation == '+':
                        return AlgebraicStructure.unpack(self_child) + other_child
                    if operation == '-':
                        return AlgebraicStructure.unpack(self_child) - other_child
                    if operation == '*':
                        return AlgebraicStructure.unpack(self_child) * other_child
                    if operation == '/':
                        return AlgebraicStructure.unpack(self_child) / other_child
                    if operation == 'compose':
                        return DifferentiableFunction.compose(AlgebraicStructure.unpack(self_child), other_child)
            else:
                if other_child is AlgebraicStructure:
                    # self is a function, other is a structure
                    if operation == '+':
                        return self_child + AlgebraicStructure.unpack(other_child)
                    if operation == '-':
                        return self_child - AlgebraicStructure.unpack(other_child)
                    if operation == '*':
                        return self_child * AlgebraicStructure.unpack(other_child)
                    if operation == '/':
                        return self_child / AlgebraicStructure.unpack(other_child)
                    if operation == 'compose':
                        return DifferentiableFunction.compose(self_child, AlgebraicStructure.unpack(other_child))
                else:
                    # both children are functions
                    if operation == '+':
                        return self_child + other_child
                    if operation == '-':
                        return self_child - other_child
                    if operation == '*':
                        return self_child * other_child
                    if operation == '/':
                        return self_child / other_child
                    if operation == 'compose':
                        return DifferentiableFunction.compose(self_child, other_child)
        else:
            return operation

    ####################
    ## Calculus Rules ##
    ####################

    def productRule(self, other):
        first_term = AlgebraicStructure.differentiate(self) * other
        second_term = self * AlgebraicStructure.differentiate(other)
        return first_term + second_term

    def quotientRule(self, other):
        first_num = AlgebraicStructure.differentiate(self) * other
        second_num = self * AlgebraicStructure.differentiate(other)
        num = first_num - second_num
        denom = other * other
        return num / denom

    def chainRule(self, other):
        deriv_outside = AlgebraicStructure.differentiate(self)
        first_term = AlgebraicStructure.compose(deriv_outside, other)
        second_term = AlgebraicStructure.differentiate(other)
        return first_term * second_term

    def applyDerRule(self, other, operation):
        if operation == '+':
            return AlgebraicStructure.differentiate(self) + AlgebraicStructure.differentiate(other)
        if operation == '-':
            return AlgebraicStructure.differentiate(self) - AlgebraicStructure.differentiate(other)
        rule_dict = {
            '*': AlgebraicStructure.productRule,
            '/': AlgebraicStructure.quotientRule,
            'compose': AlgebraicStructure.chainRule
        }
        return rule_dict[operation](self, other)
    
    def differentiate(self):
        operation = self.root
        if operation in ['+', '*', '-', '/', 'compose']:
            self_child, other_child = self.self_child, self.other_child
            if self_child is AlgebraicStructure:
                if other_child is AlgebraicStructure:
                    # Both children are algebraic structures
                    return AlgebraicStructure.applyDerRule(self_child, other_child, operation)
                else:
                    # self is a structure, other is a function
                    if operation == '+':
                        return AlgebraicStructure.differentiate(self_child) + type(other_child).derivative(other_child)
                    if operation == '-':
                        return AlgebraicStructure.differentiate(self_child) - type(other_child).derivative(other_child)
                    if operation == '*':
                        first_term = AlgebraicStructure.differentiate(self_child) * other_child
                        second_term = AlgebraicStructure.unpack(self_child) * type(other_child).derivative(other_child)
                        return first_term + second_term
                    if operation == '/':
                        first_num = AlgebraicStructure.differentiate(self_child) * other_child
                        second_num = AlgebraicStructure.unpack(self_child) * type(other_child).derivative(other_child)
                        num = first_num - second_num
                        denom = other_child * other_child
                        return num / denom
                    if operation == 'compose':
                        deriv_outside = AlgebraicStructure.differentiate(self_child)
                        first_term = DifferentiableFunction.compose(deriv_outside, other_child)
                        second_term = type(other_child).derivative(other_child)
                        return first_term * second_term
            else:
                if other_child is AlgebraicStructure:
                    # self is a function, other is a structure
                    if operation == '+':
                        return type(self_child).derivative(self_child) + AlgebraicStructure.differentiate(other_child)
                    if operation == '-':
                        return type(self_child).derivative(self_child) - AlgebraicStructure.differentiate(other_child)
                    if operation == '*':
                        first_term = type(self_child).derivative(self_child) * AlgebraicStructure.unpack(other_child)
                        second_term = self_child * AlgebraicStructure.differentiate(other_child)
                        return first_term + second_term
                    if operation == '/':
                        first_num = type(self_child).derivative(self_child) * AlgebraicStructure.unpack(other_child)
                        second_num = self_child * AlgebraicStructure.differentiate(other_child)
                        num = first_num - second_num
                        denom = AlgebraicStructure.unpack(other_child) * AlgebraicStructure.unpack(other_child)
                        return num / denom
                    if operation == 'compose':
                        deriv_outside = type(self_child).derivative(self_child)
                        first_term = DifferentiableFunction.compose(deriv_outside, AlgebraicStructure.unpack(other_child))
                        second_term = AlgebraicStructure.differentiate(other_child)
                        return first_term * second_term
                else:
                    # both children are functions
                    return DifferentiableFunction.applyDerRule(self_child, other_child, operation)
        else:
            func = operation
            return type(func).derivative(func)

    ################################
    ## Graph Theoretic Operations ##
    ################################

    def changeWeight(self, edge, weight):
        assert edge in self.weights, "Input tuple is not an edge"
        self.weights[edge] = weight
    
    ##########################
    ## Algebraic Operations ##
    ##########################

    def __add__(self, other):
        return AlgebraicStructure('+', self, other)
    
    def __mul__(self, other):
        return AlgebraicStructure('*', self, other)
    
    def __sub__(self, other):
        d = AlgebraicStructure('-', self, other)
        d.changeWeight((d.root, self), 'self')
        d.changeWeight((d.root, other), 'other')
        return d
    
    def __truediv__(self, other):
        f = AlgebraicStructure('/', self, other)
        f.changeWeight((f.root, self), 'self')
        f.changeWeight((f.root, other), 'other')
        return f
    
    def compose(self, other):
        c = AlgebraicStructure('compose', self, other)
        c.changeWeight((c.root, self), 'self')
        c.changeWeight((c.root, other), 'other')
        return c


class Exponential(DifferentiableFunction):
    def __init__(self, argument, coeff, base):
        assert base > 0, "Base needs to be positive"
        self.coeff = coeff
        self.base = base
        structure = AlgebraicStructure(self)
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
        structure = AlgebraicStructure(self)
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
        return Polynomial(self.argument, deriv_coeffs)
    

class Trigonometric(DifferentiableFunction):
    def __init__(self, argument, coeff, flavor):
        '''
        Last argument determines sine or cosine:
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
        structure = AlgebraicStructure(self)
        DifferentiableFunction.__init__(
            self,
            argument,
            rule,
            structure
        )

    def __str__(self):
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
import math
import random
from structure import AlgebraicStructure

class DifferentiableFunction():
    def __init__(self, rule):
        self.rule = rule
        self.structure = AlgebraicStructure(rule)

    def evaluate(self, input):
        return self.rule(input)
    
    def __add__(self, other):
        s_rule = lambda x: self.rule(x) + other.rule(x)
        s = DifferentiableFunction(s_rule)
        s.structure = self.structure + other.structure
        return s
    
    def derivative(self):
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
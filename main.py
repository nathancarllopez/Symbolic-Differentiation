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
    

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


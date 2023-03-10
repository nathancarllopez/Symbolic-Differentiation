import math
import thirdtry as T

cubed = T.RealPowers(1, 3)
ln = T.Logarithms(math.e)
poly = T.Polynomial([5, 0, 9])

# F = ln(5x^2 + 9)^3
f = T.DifferentiableFunction.compose(ln, poly)
g = T.DifferentiableFunction.compose(cubed, f)

print("Original\n", f)
print("Derivative\n", f.differentiate())
# print()
# print("Original\n", g)
# print("Derivative\n", g.differentiate())

print("original\n", ln)
print("derivative\n", ln.differentiate())
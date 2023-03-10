import thirdtry as T

poly = T.Polynomial([2, 0, 3, -1])
exp = T.Exponential(3, 5)

f = poly + exp
g = poly * exp
h = poly / exp
k = T.DifferentiableFunction.compose(poly, exp)

for x in [f,g,h,k]:
    print("Original\n", x)
    print("Derivative\n", x.differentiate())
    print()
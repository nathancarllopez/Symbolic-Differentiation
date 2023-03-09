import classes as c

poly = c.Polynomial('x', [1, 5, 0, -3])
exp = c.Exponential('x', 2, 2)
sin = c.Trigonometric('x', 2, 's')

f = poly + exp
g = poly + exp + sin
h = f + sin

for x in [f,g,h]:
    print("original:", x)
    print("derivative:", x.differentiate())
    print()
class WeightedTree():
    def __init__(self, vertices):
        '''
        A weighted graph (hereafter 'graph') is created by first specifying a list of vertices.
        Edges are added manually by specifying a starting and ending vertex

        Parameters
        ----------
        vertices : list
            The vertices of the digraph

        Attributes
        ----------
        self.vertices : list
            The same list as vertices
        self.num_vertices : int
            len(self.vertices)
        self.edges : list
            Initially empty list, will contain tuples of vertices
        self.weights : dictionary
            The edges in the graph are the keys of self.weights

        '''
        self.vertices = vertices
        self.num_vertices = len(vertices)
        self.edges = []
        self.weights = {}

    def add_edge(self, v0, v1):
        '''
        Note that the edges are directed, which is fine since, for
        our purposes, we'll only think of trees. All edges flow
        outward from the root towards the leaves
        '''
        self.edges.append((v0, v1))
        self.weights[(v0, v1)] = 1

    def change_weight(self, edge, new_weight):
        self.weights[edge] = new_weight

    def get_children(self, v):
        edges = [edge for edge in self.edges if v in edge]
        children = [w for (v, w) in edges]
        return children
    
    def __str__(self):
        vertices_str = "The vertices of the graph are " + str(self.vertices) + ".\n"
        edges_str = "The edges of the graph are " + str(self.edges) + ".\n"
        weights_str = "The weights of each edge are " + str(self.weights) + "."
        return vertices_str + edges_str + weights_str
    

class AlgebraicStructure(WeightedTree):
    def __init__(self, vertices, rules):
        '''
        A weighted tree representing the way that a differentiable function
        is put together algebraically.

        Inputs:
            vertices (list)
            A list of labels. There is one root vertex labeled "R" and at
            least one leaf vertex labeled "L". All other vertices correspond
            to an operation: +, -, *, /, composition

            rules (dictionary)
            The keys are tuples of vertices, and the values are functions 
            that give the output of the differentiable function

        Example:
            f(x) = 3x^2 + 2^x
            vertices = ['R', '+', 'L_poly', 'L_exp']
            rules = {
            ('+', 'L_poly'): 3x^2,
            ('+', 'L_exp'): 2^x
            }
        '''
        self.rules = rules
        self.vertices = vertices
        WeightedTree.__init__(self, vertices)
        for edge in rules:
            self.add_edge(edge[0], edge[1])
            self.change_weight(edge, rules[edge])

    def __add__(self, other):
        new_operation = '+'
        new_vertices = ['R', new_operation] + [(v, 'self') for v in self.vertices if v != 'R'] + [(v, 'other') for v in other.vertices if v != 'R']
        new_rules = {('R', new_operation): 1}
        for (v, w) in self.rules:
            if v == 'R':
                new_rules[(new_operation, (w, 'self'))] = self.rules[(v, w)]
            else:
                new_rules[((v, 'self'), (w, 'self'))] = self.rules[(v, w)]
        for (v, w) in other.rules:
            if v == 'R':
                new_rules[(new_operation, (w, 'other'))] = other.rules[(v, w)]
            else:
                new_rules[((v, 'self'), (w, 'self'))] = other.rules[(v, w)]
        s = AlgebraicStructure(new_vertices, new_rules)
        return s
    
f = AlgebraicStructure(['R', 'L'], {('R', 'L'): lambda x: 3 * x * x})
g = AlgebraicStructure(['R', 'L'], {('R', 'L'): lambda x: 4 ** x})
h = f+g
k = h + h
for x in [f, g, h, k]:
    print(x)
    print()
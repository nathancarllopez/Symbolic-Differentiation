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

    def change_weight(self, v0, v1, new_weight):
        self.weights[(v0, v1)] = new_weight

    def get_children(self, v):
        edges = [edge for edge in self.edges if v in edge]
        children = [w for (v, w) in edges]
        return children
    

class AlgebraicStructure(WeightedTree):
    def __init__(self, vertices, rules):
        self.rules = rules
        WeightedTree.__init__(self, ['R', 'L'])
        self.add_edge('R', 'L')
        self.change_weight('R', 'L', rule)

    def __add__(self, other):
        s = WeightedTree(['R', '+', 'L_self', 'L_other'])
        
        return s
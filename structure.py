class WeightedGraph():
    def __init__(self, vertices):
        '''
        A weighted graph (hereafter 'graph') is created by first specifying a list of vertices.
        Edges are added manually by specifying a starting and ending vertex

        Parameters
        ----------
        vertices : list
            The vertices of the tree

        Attributes
        ----------
        self.vertices : list
            The same list as vertices
        self.edges : list
            Initially empty list, will contain tuples of vertices
        self.weights : dictionary
            The edges in the graph are the keys of self.weights

        '''
        self.vertices = vertices
        self.edges = []
        self.weights = {}

    def add_edge(self, v0, v1):
        self.edges.append((v0, v1))

    def change_weight(self, edge, new_weight):
        self.weights[edge] = new_weight

    def __str__(self):
        vertices_str = "The vertices of the graph are " + str(self.vertices) + ".\n"
        edges_str = "The edges of the graph are " + str(self.edges) + ".\n"
        weights_str = "The weights on the edges are " + str(self.weights) + "."
        return vertices_str + edges_str + weights_str

class AlgebraicStructure(WeightedGraph):
    def __init__(self, root, other_vertices):
        self.root = root
        self.other_vertices = other_vertices
        WeightedGraph.__init__(self, [root] + other_vertices)

    def __add__(self, other):
        s = AlgebraicStructure('+', self.vertices + other.vertices)
        s.edges = self.edges + other.edges
        for key in self.weights:
            s.weights[key] = self.weights[key]
        for key in other.weights:
            s.weights[key] = other.weights[key]
        s.add_edge('+', self.root)
        s.add_edge('+', other.root)
        return s

    def get_subtrees_below_root(self):
        pass
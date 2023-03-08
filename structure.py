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
        vertices_str = 'The vertices of the graph are '
        vertices_str += ', '.join(list(map(str, self.vertices)))
        vertices_str += '.\n'

        if len(self.edges) > 0:
            edges_str = 'The edges of the graph are '
            edges_str += ','.join(list(map(str, self.edges)))
            edges_str += '.\n'
            if len(self.weights) > 0:
                weights_str = 'The weights on each edge are '
                weights_str += ','.join(list(map(str, self.weights.items())))
            else:
                weights_str = 'None of the edges have weights.'
        else:
            edges_str = 'There are no edges.\n'
            weights_str = ''

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
    
    def get_children(self, vertex):
        children = []
        for edge in self.edges:
            if edge[0] == vertex:
                children.append(edge[1])
        return children
    
    def get_descendants(self, vertex):
        descendants = self.get_children(vertex)
        next_generation = []
        if len(descendants) == 0:
            return next_generation
        for child in descendants:
            next_generation.extend(self.get_descendants(child))
        return next_generation

    def get_subtrees_below_root(self):
        if self.get_descendants(self.root) == self.root:
            return self
        subtrees = []
        stems = self.get_children(self.root)
        for stem in stems:
            vertices = self.get_descendants(stem)
            subtree = AlgebraicStructure(stem, vertices)
            for edge in self.edges:
                if edge[0] in [stem] + vertices:
                    subtree.add_edge(edge[0], edge[1])
            for edge in self.weights:
                if edge in subtree.edges:
                    subtree.weights[edge] = self.weights[edge]
            subtrees.append(subtree)
        return subtrees
    
    def __str__(self):
        return WeightedGraph.__str__(self)
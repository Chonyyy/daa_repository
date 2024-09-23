import networkx as nx
import matplotlib.pyplot as plt
import random as rnd


class Graph:
    def __init__(self):
        self.graph = nx.Graph()
        """The networkx graph instance"""

    def add_vertex(self, vertex):
        """Adds a vertex to the graph"""
        self.graph.add_node(vertex)

    def add_edge(self, vertex1, vertex2):
        """Adds an edge between 2 vertex in the graph"""
        self.graph.add_edge(vertex1, vertex2)

    def remove_vertex(self, vertex):
        """Removes the vertex and all adjacent edges. Attempting to remove a nonexistent vertex will raise an exception."""
        self.graph.remove_node(vertex)

    def remove_edge(self, vertex1, vertex2):
        """Remove an edge"""
        self.graph.remove_edge(vertex1, vertex2)

    def __getitem__(self, vertex):
        """Returns the adjacency list of the vertex"""
        if vertex in self.graph:
            return set(self.graph.neighbors(vertex))
        else:
            raise KeyError(f"Vertex {vertex} not found in graph")

    def has_vertex(self, vertex) -> bool:
        """Returns True if the graph contains the vertex"""
        return self.graph.has_node(vertex)

    def has_edge(self, vertex1, vertex2) -> bool:
        """Returns True if the graph has te edge (vertex1, vertex2)"""
        return self.graph.has_edge(vertex1, vertex2)

    def __len__(self):
        return self.graph.number_of_nodes()

    def num_edges(self):
        """Returns the number of edges in the graph"""
        return self.graph.number_of_edges()

    def get_vertices(self):
        """Returns all the vertices of the graph as a list"""
        return list(self.graph.nodes())

    def get_edges(self):
        """Returns all the edges of the graph as a list"""
        return list(self.graph.edges())


    def get_vertex_degrees(self):
        """Returns a dictionary with vertices as keys and their degrees as values"""
        return dict(self.graph.degree())

    def subgraph(self, vertices):
        """Given a set of vertices it returns the subgraph of the actual graph
        with only those edges"""
        sub_g = Graph()
        sub_g.graph = self.graph.subgraph(vertices).copy()
        return sub_g

    def draw_graph(
        self,
        ax = None,
        edge_color_map=None,
        edge_width_map=None,
        edge_alphas=None,
        node_size_map=None,
    ):
        """Draws a graph"""
        pos = nx.spring_layout(self.graph)
        edges = self.graph.edges()

        is_ax_none = False
        if ax is None:
            fig, ax = plt.subplots()
            is_ax_none = True

        if edge_color_map is None:
            edge_color_map = {}
        if edge_width_map is None:
            edge_width_map = {}
        if edge_alphas is None:
            edge_alphas = [1.0] * len(edges)
        if node_size_map is None:
            node_size_map = {node: 300 for node in self.graph.nodes()}

        edge_colors = []
        edge_widths = []
        for edge in edges:
            if edge in edge_color_map:
                edge_colors.append(edge_color_map[edge])
            elif (edge[1], edge[0]) in edge_color_map:
                edge_colors.append(edge_color_map[(edge[1], edge[0])])
            else:
                edge_colors.append("black")

            if edge in edge_width_map:
                edge_widths.append(edge_width_map[edge])
            elif (edge[1], edge[0]) in edge_width_map:
                edge_widths.append(edge_width_map[(edge[1], edge[0])])
            else:
                edge_widths.append(1.0)

        nx.draw_networkx_edges(
            self.graph,
            pos,
            edgelist=edges,
            edge_color=edge_colors,
            width=edge_widths,
            alpha=edge_alphas,
            ax=ax,
        )
        nx.draw_networkx_nodes(
            self.graph,
            pos,
            node_size=[node_size_map[node] for node in self.graph.nodes()],
            ax=ax,
        )
        nx.draw_networkx_labels(self.graph, pos, ax=ax)
        
        if is_ax_none:
            plt.show()


def draw_two_graphs(
    graph1,
    graph2,
    edge_color_map1=None,
    edge_width_map1=None,
    node_size_map1=None,
    edge_color_map2=None,
    edge_width_map2=None,
    node_size_map2=None,
):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    graph1.draw_graph(
        ax1,
        edge_color_map=edge_color_map1,
        edge_width_map=edge_width_map1,
        node_size_map=node_size_map1,
    )
    graph2.draw_graph(
        ax2,
        edge_color_map=edge_color_map2,
        edge_width_map=edge_width_map2,
        node_size_map=node_size_map2,
    )

    ax1.set_title("Graph A")
    ax2.set_title("Graph B")

    plt.show()


def generate_random_graph(n: int = 10, m: int = 40) -> Graph:
    """Generate a random graph"""
    g = Graph()
    n = max(1, n)
    indexes = [i for i in range(n)]
    for index in indexes:
        g.add_vertex(index)

    max_edges = int(n * (n - 1) / 2)
    m = min(max_edges, max(0, m))

    for _ in range(m):
        while True:
            a, b = rnd.sample(indexes, 2)
            if not g.has_edge(a,b):
                g.add_edge(a,b)
                break

    return g

import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.graph = nx.Graph()

    def add_vertex(self, vertex):
        self.graph.add_node(vertex)

    def add_edge(self, vertex1, vertex2):
        self.graph.add_edge(vertex1, vertex2)

    def remove_vertex(self, vertex):
        self.graph.remove_node(vertex)

    def remove_edge(self, vertex1, vertex2):
        self.graph.remove_edge(vertex1, vertex2)

    def draw_graph(self, ax, edge_color_map=None, edge_width_map=None, edge_alphas=None, node_size_map=None):
        pos = nx.spring_layout(self.graph)
        edges = self.graph.edges()
        
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
                edge_colors.append('black')
            
            if edge in edge_width_map:
                edge_widths.append(edge_width_map[edge])
            elif (edge[1], edge[0]) in edge_width_map:
                edge_widths.append(edge_width_map[(edge[1], edge[0])])
            else:
                edge_widths.append(1.0)
        
        nx.draw_networkx_edges(self.graph, pos, edgelist=edges, edge_color=edge_colors, width=edge_widths, alpha=edge_alphas, ax=ax)
        nx.draw_networkx_nodes(self.graph, pos, node_size=[node_size_map[node] for node in self.graph.nodes()], ax=ax)
        nx.draw_networkx_labels(self.graph, pos, ax=ax)

def draw_two_graphs(graph1, graph2, edge_color_map1=None, edge_width_map1=None, node_size_map1=None, edge_color_map2=None, edge_width_map2=None, node_size_map2=None):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    graph1.draw_graph(ax1, edge_color_map=edge_color_map1, edge_width_map=edge_width_map1, node_size_map=node_size_map1)
    graph2.draw_graph(ax2, edge_color_map=edge_color_map2, edge_width_map=edge_width_map2, node_size_map=node_size_map2)
    
    ax1.set_title('Graph A')
    ax2.set_title('Graph B')
    
    plt.show()

# Ejemplo de uso
g1 = Graph()
g1.add_vertex('A')
g1.add_vertex('B')
g1.add_vertex('C')
g1.add_edge('A', 'B')
g1.add_edge('A', 'C')
g1.add_edge('B', 'C')

g2 = Graph()
g2.add_vertex('D')
g2.add_vertex('E')
g2.add_vertex('F')
g2.add_edge('D', 'E')
g2.add_edge('E', 'F')

# Definir colores y grosores para las aristas del primer grafo
edge_color_map1 = {('A', 'B'): 'red', ('A', 'C'): 'blue'}
edge_width_map1 = {('A', 'B'): 2.0, ('A', 'C'): 3.0}
node_size_map1 = {'A': 500, 'B': 700, 'C': 900}

# Definir colores y grosores para las aristas del segundo grafo
edge_color_map2 = {('D', 'E'): 'green', ('E', 'F'): 'purple'}
edge_width_map2 = {('D', 'E'): 2.5, ('E', 'F'): 3.5}
node_size_map2 = {'D': 600, 'E': 800, 'F': 1000}

draw_two_graphs(g1, g2, edge_color_map1=edge_color_map1, edge_width_map1=edge_width_map1, node_size_map1=node_size_map1, edge_color_map2=edge_color_map2, edge_width_map2=edge_width_map2, node_size_map2=node_size_map2)

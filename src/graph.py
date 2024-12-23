import networkx as nx
import matplotlib.pyplot as plt
import math

class Graph:
    def __init__(self, nodes: dict):
        self.K = nx.Graph()
        self.pos = {node: coord for node, coord in nodes.items()}

        for node, coord in nodes.items():
            self.K.add_node(node, pos=coord)

        for node1, coord1 in nodes.items():
            for node2, coord2 in nodes.items():
                if node1 != node2:
                    distance = math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)
                    self.K.add_edge(node1, node2, weight=distance)

    def draw(self, file_path, title):
        plt.figure(figsize=(14, 10)) 
        plt.title(title, fontsize=12, fontweight='bold')

        nx.draw_networkx_nodes(self.K, self.pos, node_color='lightblue', node_size=300)
        nx.draw_networkx_labels(self.K, self.pos, font_weight='bold', font_size=8)

        plt.savefig(file_path)
        plt.close() 
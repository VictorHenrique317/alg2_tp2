import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np
import pickle

class Graph:
    def __init__(self, nodes: dict):
        if nodes == {}:
            return
        
        print(f"-> Creating graph for {len(nodes)} nodes")
        self.nodes = nodes
        self.K = nx.Graph()
        self.pos = {node: coord for node, coord in nodes.items()}
        self.K.add_nodes_from(self.pos.keys())

        # self.K.add_weighted_edges_from(edges)
        print(f"-> Graph created for {len(nodes)} nodes")

    def calculate_distances(self): # Heavy computation
        node_labels = list(self.nodes.keys())
        coordinates = np.array(list(self.nodes.values()))

        num_nodes = len(node_labels)
        edges = []
        print(f"-> Calculating distances in chunks to optimize memory usage...")
        line = 0
        for i in range(num_nodes):
            line += 1
            for j in range(i + 1, num_nodes):
                distance = np.linalg.norm(coordinates[i] - coordinates[j])
                edges.append((node_labels[i], node_labels[j], distance))

            if i % 100 == 0:
                print(f"\tProcessed {100*line/num_nodes: .2f}% of the total matrix lines...", end='\r')

        print(end='\n')
        print(f"-> Computed distances for {len(node_labels)} nodes")

    @staticmethod
    def load(filepath: str):
        with open(filepath, 'rb') as file:
            data = pickle.load(file)
        graph = Graph({})
        graph.K = data['graph']
        graph.pos = data['pos']
        print(f"Graph loaded from {filepath}")
        return graph
    
    def save(self, filepath: str):
        data = {
            'graph': self.K,
            'pos': self.pos
        }
        with open(filepath, 'wb') as file:
            pickle.dump(data, file)
        print(f"Graph saved to {filepath}")

    def draw(self, file_path, title):
        plt.figure(figsize=(14, 10))
        plt.title(title, fontsize=12, fontweight='bold')

        nx.draw_networkx_nodes(self.K, self.pos, node_color='lightblue', node_size=300)
        nx.draw_networkx_labels(self.K, self.pos, font_weight='bold', font_size=8)

        plt.savefig(file_path)
        plt.close() 
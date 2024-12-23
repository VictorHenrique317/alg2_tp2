import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pickle

class Graph:
    def __init__(self, nodes: dict):
        if nodes == {}:
            return
        
        print(f"-> Creating graph for {len(nodes)} nodes")
        self.calculated_distances = False
        self.K = nx.Graph()
        self.pos = {node: coord for node, coord in nodes.items()}
        self.K.add_nodes_from(self.pos.keys())

        print(f"-> Graph created for {len(nodes)} nodes")

    def get_distance(self, u, v) -> float:
        if self.calculated_distances == True:
            edge_data = self.K.get_edge_data(u, v)
            return edge_data['weight']

        u_x = self.pos[u][0]
        u_y = self.pos[u][1]

        v_x = self.pos[v][0]
        v_y = self.pos[v][1]

        return np.linalg.norm(np.array([v_x, v_y]) - np.array([u_x, u_y]))
    
    def get_nodes(self):
        return list(self.pos.keys())
    
    def get_coordinates(self):
        return list(self.pos.values())

    def calculate_distances(self): # Heavy computation
        node_labels = self.get_nodes()
        coordinates = np.array(self.get_coordinates())

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
        
        self.calculated_distances = True 
        self.K.add_weighted_edges_from(edges)

    @staticmethod
    def load(filepath: str):
        with open(filepath, 'rb') as file:
            data = pickle.load(file)
        graph = Graph({})
        graph.K = data['graph']
        graph.pos = data['pos']
        graph.calculated_distances = data['calculated_distances']
        print(f"Graph loaded from {filepath}")
        return graph
    
    def save(self, filepath: str):
        data = {
            'graph': self.K,
            'pos': self.pos,
            'calculated_distances': self.calculated_distances
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
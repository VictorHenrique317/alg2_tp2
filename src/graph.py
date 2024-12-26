import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pickle

class Graph:
    def __init__(self, nodes: dict):
        """
        Initializes a graph with the given nodes.

        Args:
            nodes (dict): A dictionary where keys are node identifiers and values are their coordinates.
        Returns:
            None
        If the nodes dictionary is empty, the function returns immediately without creating a graph.
        Otherwise, it initializes a graph, sets up node positions, and adds nodes to the graph.
        Attributes:
            calculated_distances (bool): A flag indicating whether distances have been calculated and stored in memory.
            K (networkx.Graph): The graph object.
            pos (dict): A dictionary mapping nodes to their coordinates.
        """
        if nodes == {}:
            return
        
        print(f"-> Creating graph for {len(nodes)} nodes")
        self.calculated_distances = False
        self.K = nx.Graph()
        self.pos = {node: coord for node, coord in nodes.items()}
        self.K.add_nodes_from(self.pos.keys())

        print(f"-> Graph created for {len(nodes)} nodes")

    def get_distance(self, u, v) -> float:
        """
        Calculate the distance between two nodes u and v.
        If the distances have already been calculated and stored, it retrieves the 
        distance from the edge data. Otherwise, it calculates the Euclidean distance 
        between the positions of the two nodes.

        Args:
            u: The first node.
            v: The second node.
        Returns:
            float: The distance between node u and node v.
        """
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
        """
        Calculate the distances between all pairs of nodes in the graph.
        This method performs a heavy computation to calculate the Euclidean distances
        between all pairs of nodes in the graph. The distances are computed one-by-one
        to optimize memory usage. The computed distances are then added as weighted
        edges to the graph.
        The method prints progress updates to the console to indicate the percentage
        of the total matrix lines processed.

        Args:
            calculated_distances (bool): A flag indicating whether the distances have
                                         been calculated.
            K (networkx.Graph): The graph object to which the weighted edges are added.
        Raises:
            ValueError: If the number of nodes or coordinates is inconsistent.
        """
        node_labels = self.get_nodes()
        coordinates = np.array(self.get_coordinates())

        num_nodes = len(node_labels)
        edges = []
        print(f"-> Calculating distances one-by-one to optimize memory usage...")
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
        """
    Load a graph from a file.

    This method reads a graph object from a file using the pickle module.
    The file should contain a dictionary with keys 'graph', 'pos', and 'calculated_distances'.

    Args:
        filepath (str): The path to the file from which to load the graph.

    Returns:
        Graph: The graph object loaded from the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        pickle.UnpicklingError: If the file is not a valid pickle file.
    """
        with open(filepath, 'rb') as file:
            data = pickle.load(file)
        graph = Graph({})
        graph.K = data['graph']
        graph.pos = data['pos']
        graph.calculated_distances = data['calculated_distances']
        print(f"Graph loaded from {filepath}")
        return graph
    
    def save(self, filepath: str):
        """
        Saves the graph data to a file in binary format using pickle. This ables the
        user to save the graph structure, node positions, and precomputed distances, so that
        the graph can be loaded later without having to do this computation again.

        The data saved includes:
            - 'graph': The graph structure (self.K).
            - 'pos': The positions of the nodes (self.pos).
            - 'calculated_distances': The precomputed distances (self.calculated_distances).

        The file is saved in binary format.

        Args:
            filepath (str): The path to the file where the graph data will be saved.
        """
        data = {
            'graph': self.K,
            'pos': self.pos,
            'calculated_distances': self.calculated_distances
        }
        with open(filepath, 'wb') as file:
            pickle.dump(data, file)
        print(f"Graph saved to {filepath}")

    def draw(self, file_path, title):
        """
        Draws the graph and saves it to a file.
        
        Args:
            file_path (str): The path where the image file will be saved.
            title (str): The title of the graph.
        """
        plt.figure(figsize=(14, 10))
        plt.title(title, fontsize=12, fontweight='bold')

        nx.draw_networkx_nodes(self.K, self.pos, node_color='lightblue', node_size=300)
        nx.draw_networkx_labels(self.K, self.pos, font_weight='bold', font_size=8)

        plt.savefig(file_path)
        plt.close() 
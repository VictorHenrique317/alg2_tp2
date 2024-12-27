import networkx as nx

from utils import measure

@measure
def chistofides(graph, start_node, result_queue):
    """
    Solve TSP using the Christofides algorithm.
    Distances are fetched via graph.get_distance(u,v).

    Args: 
        graph (Graph): a graph object
        start_node (int): label of the node to start from; if None, pick an arbitrary node
        result_queue (multiprocessing.Queue): a multiprocessing or threading queue to store (path, cost)
    """
    # --------------------------
    # 1) Pre-processing
    # --------------------------
    graph.calculate_distances()

    if not graph.get_nodes():
        result_queue.put(([], 0.0))
        return

    mst = nx.minimum_spanning_tree(graph.K)

    odd_vertices = [node for node in mst.nodes() if mst.degree(node) % 2 != 0]
    subgraph = graph.K.subgraph(odd_vertices)

    # Invert the weight of the edges to calculate the minimum weight perfect matching
    for u, v in subgraph.edges():
        subgraph[u][v]['weight'] *= -1

    # Find minimum weight perfect matching
    min_weight_matching = nx.max_weight_matching(subgraph, maxcardinality=True)

    graph_min_matching = graph.K.edge_subgraph(min_weight_matching)

    # Create a multigraph with the vertices of G and the edges of the MST and the minimum weight perfect matching
    multigraph = nx.MultiGraph()
    multigraph.add_weighted_edges_from(mst.edges.data('weight'))
    multigraph.add_weighted_edges_from(graph_min_matching.edges.data('weight'))

    # --------------------------
    # 2) Compute the Eulerian circuit
    # --------------------------
    start_node = str(start_node)  # Ensure start_node is a string
    eulerian_circuit = [u for u, v in nx.eulerian_circuit(multigraph, source=start_node)]

    # --------------------------
    # 3) Remove duplicate vertices to construct a Hamiltonian circuit
    # --------------------------
    path = list(dict.fromkeys(eulerian_circuit))
    path.append(start_node)

    # --------------------------
    # 4) Calculate the path length
    # --------------------------
    length = sum(graph.get_distance(u, v) for u, v in zip(path, path[1:]))

    result_queue.put((path, length))
    return result_queue


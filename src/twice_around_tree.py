import networkx as nx

from utils import measure

@measure
def twice_around_tree(graph, start_node, result_queue):
    """
    Solve TSP using the Twice-Around-the-Tree heuristic.
    Distances are fetched via graph.get_distance(u,v).

    Args: 
        graph (Graph): a graph object
        start_node (int): label of the node to start from; if None, pick an arbitrary node
        result_queue (multiprocessing.Queue): a multiprocessing or threading queue to store (path, cost)
    """
    # --------------------------
    # 1) Pre-processing
    # --------------------------
    def build_adjacency_dict(graph):
        adj = {}
        for u, v in graph.edges():
            w = graph[u][v]['weight']
            adj.setdefault(u, []).append((v, w))
            adj.setdefault(v, []).append((u, w))
        return adj

    graph.calculate_distances()

    if not graph.get_nodes():
        result_queue.put(([], 0.0))
        return

    mst = nx.minimum_spanning_tree(graph.K)
    mst_adj = build_adjacency_dict(mst)

    def dfs_preorder(adjacency, start):
        visited = []
        stack = [start]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.append(node)
                for (neighbor, _) in reversed(adjacency.get(node, [])):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return visited

    if start_node is None:
        start_node = list(graph.nodes())[0]
    start_node = str(start_node)

    # --------------------------
    # 2) Compute the path
    # --------------------------
    try:
        path = dfs_preorder(mst_adj, start_node)
        path.append(start_node)

    except RecursionError as e:
        print(f"Recursion depth exceeded")

    # --------------------------
    # 3) Calculate the path length
    # --------------------------
    length = 0
    for u, v in zip(path, path[1:]):
        length += graph.get_distance(u, v)

    result_queue.put((path, length))
    return result_queue


import math

from utils import measure

@measure
def branch_and_bound(graph, start_node, result_queue):
    """
    Solve TSP using a Branch-and-Bound approach with Depth-First Search.
    Distances are fetched via graph.get_distance(u,v) on the fly.

    :param graph: a Graph object with:
                  - graph.get_nodes(): list of node labels
                  - graph.get_distance(u, v): float, distance between node u and node v
    :param start_node: label of the node to start from; if None, pick an arbitrary node
    :param result_queue: a multiprocessing or threading queue to store (best_path, best_cost)
    """
    # --------------------------
    # 1) Preliminaries
    # --------------------------
    node_list = graph.get_nodes()
    n = len(node_list)
    if n == 0:
        result_queue.put(([], 0.0))
        return
    if n == 1:
        result_queue.put((node_list, 0.0))
        return

    # Map node_label -> index
    index_of = {node: idx for idx, node in enumerate(node_list)}
    # Map index -> node_label
    label_of = {idx: node for node, idx in index_of.items()}

    # Decide on start node
    if start_node is None:
        start_node = node_list[0]
    start_node = str(start_node)  # ensure it's a string if needed
    start_idx = index_of[start_node]

    # --------------------------
    # 2) Precompute minimal outgoing edge for each node (for bounding)
    # --------------------------
    def minimal_out_edge(idx):
        """Returns the minimal distance from node_idx to any other node."""
        node_label = label_of[idx]
        min_dist = math.inf
        for other_idx in range(n):
            if other_idx == idx:
                continue
            other_label = label_of[other_idx]
            dist = graph.get_distance(node_label, other_label)
            if dist < min_dist:
                min_dist = dist
        return min_dist

    min_edge = [minimal_out_edge(i) for i in range(n)]

    # --------------------------
    # 3) A simple bounding function
    # --------------------------
    def lower_bound_estimate(cost_so_far, visited_array):
        """
        Naive bounding: current cost + sum of minimal edges from each unvisited node.
        """
        bound = cost_so_far
        for i in range(n):
            if not visited_array[i]:
                bound += min_edge[i]
        return bound

    # --------------------------
    # 4) Global best solution tracking
    # --------------------------
    best_cost = math.inf
    best_path_idx = []

    # --------------------------
    # 5) Depth-First Search (recursive)
    # --------------------------
    def dfs(current_node_idx, visited_count, current_cost, path_idx, visited_array):
        nonlocal best_cost, best_path_idx

        # If we've visited all nodes, finalize by returning to start
        if visited_count == n:
            last_label = label_of[current_node_idx]
            start_label = label_of[start_idx]
            total_cost = current_cost + graph.get_distance(last_label, start_label)
            if total_cost < best_cost:
                best_cost = total_cost
                best_path_idx = path_idx[:]
            return

        # Otherwise, branch over unvisited nodes
        for next_node_idx in range(n):
            if not visited_array[next_node_idx]:
                # Cost to move to the next node
                current_label = label_of[current_node_idx]
                next_label = label_of[next_node_idx]
                next_cost = current_cost + graph.get_distance(current_label, next_label)

                # Compute bound
                visited_array[next_node_idx] = True
                estimate = lower_bound_estimate(next_cost, visited_array)
                # If bounding is promising, recurse deeper
                if estimate < best_cost:
                    path_idx.append(next_node_idx)
                    dfs(next_node_idx, visited_count + 1, next_cost, path_idx, visited_array)
                    path_idx.pop()

                # Backtrack
                visited_array[next_node_idx] = False

    # --------------------------
    # 6) Launch DFS from the start node
    # --------------------------
    try:
        visited = [False] * n
        visited[start_idx] = True
        dfs(
            current_node_idx=start_idx,
            visited_count=1,
            current_cost=0.0,
            path_idx=[start_idx],
            visited_array=visited
        )
    except RecursionError as e:
        print(f"Recursion depth exceeded")
    # --------------------------
    # 7) Reconstruct final path (labels) & push result
    # --------------------------
    best_path_labels = [label_of[idx] for idx in best_path_idx]
    if best_path_labels:
        best_path_labels.append(start_node)  # close the loop for clarity

    result_queue.put((best_path_labels, best_cost))
    return result_queue
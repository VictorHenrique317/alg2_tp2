import math
import heapq  # for our priority queue

def branch_and_bound(graph, start_node=None):
    """
    Solve TSP using a Branch-and-Bound approach with best-first search (priority queue).
    Distances are fetched via graph.get_distance(u,v) on the fly.
    
    :param graph: a Graph object with:
                  - graph.nodes: dict {node_label: (x, y)}
                  - graph.get_distance(u, v) -> float
    :param start_node: a node label to start from. If None, pick an arbitrary node.
    :return: (best_path, best_cost)
    """
    # --------------------------
    # 1) Preliminaries
    # --------------------------
    node_list = graph.get_nodes()
    n = len(node_list)
    if n == 0:
        return [], 0.0
    if n == 1:
        return node_list, 0.0

    # Map node_label -> index
    index_of = {node: idx for idx, node in enumerate(node_list)}
    # Map index -> node_label
    label_of = {idx: node for node, idx in index_of.items()}

    # Decide on start node
    if start_node is None:
        start_node = node_list[0]
    start_node = str(start_node)
    start_idx = index_of[start_node]

    # --------------------------
    # 2) Precompute minimal outgoing edge for each node (for bounding)
    #    This is O(n^2) in the worst case, but uses far less memory than a full matrix.
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
        Naive bounding: current cost plus the minimal edge for each unvisited node.
        """
        bound = cost_so_far
        for i in range(n):
            if not visited_array[i]:
                bound += min_edge[i]
        return bound

    # --------------------------
    # 4) Priority Queue Initialization
    #    Each state = (bound, cost, visited_count, last_node_idx, path_idx, visited_array)
    # --------------------------
    best_cost = math.inf
    best_path_idx = []

    # visited array for the start state
    visited_start = [False] * n
    visited_start[start_idx] = True

    # initial path
    init_path = [start_idx]
    init_cost = 0.0
    init_visited_count = 1

    # initial bound
    init_bound = lower_bound_estimate(init_cost, visited_start)

    # Priority queue (min-heap) of states
    # We'll push a tuple (bound, cost, visited_count, last_node_idx, path_idx, visited_array)
    pq = []
    heapq.heappush(
        pq,
        (init_bound, init_cost, init_visited_count, start_idx, init_path, visited_start)
    )

    # --------------------------
    # 5) Best-First Search
    # --------------------------
    while pq:
        # Pop the state with the smallest bound
        bound, cost, visited_count, last_node_idx, path_idx, visited_array = heapq.heappop(pq)

        # If this state's bound is already >= best_cost, we can prune all further expansions
        if bound >= best_cost:
            break

        # If we've visited all nodes, finalize by returning to start node
        if visited_count == n:
            # compute the cost to go back to start node
            last_label = label_of[last_node_idx]
            start_label = label_of[start_idx]
            final_cost = cost + graph.get_distance(last_label, start_label)

            if final_cost < best_cost:
                best_cost = final_cost
                best_path_idx = path_idx
            continue

        # Otherwise, branch by visiting each unvisited neighbor
        for next_node_idx in range(n):
            if not visited_array[next_node_idx]:
                last_label = label_of[last_node_idx]
                next_label = label_of[next_node_idx]
                next_cost = cost + graph.get_distance(last_label, next_label)

                # Build next visited array (copy)
                next_visited = visited_array[:]
                next_visited[next_node_idx] = True

                # Estimate new bound
                next_bound = lower_bound_estimate(next_cost, next_visited)
                if next_bound < best_cost:
                    # Construct new path
                    next_path = path_idx + [next_node_idx]
                    # Push the new state
                    heapq.heappush(
                        pq,
                        (
                            next_bound,
                            next_cost,
                            visited_count + 1,
                            next_node_idx,
                            next_path,
                            next_visited
                        )
                    )

    # --------------------------
    # 6) Reconstruct final path (labels)
    # --------------------------
    best_path_labels = [label_of[idx] for idx in best_path_idx]
    if best_path_labels:
        best_path_labels.append(start_node)  # close the loop for clarity

    return best_path_labels, best_cost

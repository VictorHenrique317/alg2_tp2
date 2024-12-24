from multiprocessing import Process, Queue
import time
from branch_and_bound import *
from graph import Graph
import os
import contextlib
import os
import functools
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import sys

def parse_file(file_path: str) -> dict:
    nodes = dict()
    with open(file_path, 'r') as file:
        lines = file.read()
        lines = lines.split("NODE_COORD_SECTION\n")[1]
        lines = lines.split("EOF")[0]
        lines = lines.split("\n")
        
        for i, line in enumerate(lines):
            if i % 1000 == 0:
                # print(f"\tProcessed {100*i/len(lines): .2f}% of the total lines...", end='\r')
                pass

            line = line.strip().split(" ")
            line = list(filter(None, line)) # remove empty strings from list
            if line == []:
                continue

            try:
                node = line[0]
                x = line[1]
                y = line[2]
            except IndexError as e:
                print(f"Error in line: {line}")
                raise e

            nodes[node] = (float(x), float(y))

    return nodes

def create_graph(file_path):
    nodes = parse_file(file_path)
    graph = Graph(nodes)
    return graph

def save_graphs_into_disk(): # Just needed once 
    base_dir = "test_data"
    test_files = os.listdir(base_dir)
    progress = 0
    for test_file in test_files:
        progress += 1
        print(f"Processing file: {test_file}")
        graph = create_graph(f'{base_dir}/{test_file}')
        if len(graph.get_nodes()) > 5000:
            print("Skipping file due to high number of nodes...")
            continue
        graph.calculate_distances()
        
        title = test_file.replace(".", "_")
        graph.draw(f"plots/graphs/{title}.png", title)
        graph.save(f"graphs/{title}.pkl")

        print(f'({100*progress/len(test_files): .2f}% done...)\n')

if __name__ == '__main__':
    sys.setrecursionlimit(1500)
    base_dir = "graphs"
    graph_pickles = os.listdir(base_dir)

    # save_graphs_into_disk()

    for pickle in graph_pickles:
        # if pickle != "d1291_tsp.pkl":
        #     continue
        # nodes = {
        #     "1": (16.47, 96.10),
        #     "2": (16.47, 94.44),
        #     "3": (20.09, 92.54),
        #     "4": (22.39, 93.37),
        #     "5": (25.23, 97.24),
        #     "6": (22.00, 96.05),
        #     "7": (20.47, 97.02),
        #     "8": (17.20, 96.29),
        #     "9": (16.30, 97.38),
        #     "10": (14.05, 98.12),
        #     "11": (16.53, 97.38),
        #     "12": (21.52, 95.59),
        #     "13": (19.41, 97.13),
        #     "14": (20.09, 94.55),
        # }
        # Best route found: ['1', '10', '9', '11', '8', '13', '7', '12', '6', '5', '4', '3', '14', '2', '1']
        # Best cost: 30.878503892588

        # nodes = {
        #     "1": (16.47, 96.10),
        #     "2": (16.47, 94.44),
        #     "3": (20.09, 92.54),
        #     "4": (22.39, 93.37),
        #     "5": (25.23, 97.24),
        #     "6": (22.00, 96.05),
        # }

        # graph = Graph(nodes)
        graph = Graph.load(f'{base_dir}/{pickle}')

        result_queue = Queue()

        # Create a new process
        process = Process(target=branch_and_bound, args=(graph, 1, result_queue))
        process.start()

        # Wait for the process to complete or timeout
        process.join(timeout=1800)  # 30 minutes

        if process.is_alive():
            print("Function timed out. Terminating process...")
            process.terminate()  # Forcefully terminate the process
            process.join()  # Ensure the process finishes cleanly
        else:
            # Retrieve the result from the queue if the function finished in time
            if not result_queue.empty():
                best_route, best_cost = result_queue.get()
                print(f"INFO: Best Route: {best_route}, Best Cost: {best_cost}")
            else:
                print("No result was returned.")
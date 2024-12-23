from graph import Graph
import os

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
        
        title = test_file.replace(".", "_")
        graph.draw(f"plots/graphs/{title}.png", title)
        graph.save(f"graphs/{title}.pkl")

        print(f'({100*progress/len(test_files): .2f}% done...)\n')

if __name__ == '__main__':
    pass
from graph import Graph
import os

def parse_file(file_path: str) -> dict:
    nodes = dict()
    with open(file_path, 'r') as file:
        lines = file.read()
        lines = lines.split("NODE_COORD_SECTION\n")[1]
        lines = lines.split("EOF")[0]
        lines = lines.split("\n")
        
        for line in lines:
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

if __name__ == '__main__':
    # nodes = parse_file('data/eil51.tsp')
    # graph = Graph(nodes)
    # graph.draw()

    base_dir = "../test_data"
    test_files = os.listdir(base_dir)
    progress = 0
    for test_file in test_files:
        print(f"Processing file: {test_file}")
        progress += 1
        nodes = parse_file(f'{base_dir}/{test_file}')

        graph = Graph(nodes)
        title = test_file.replace(".", "_")
        graph.draw(f"../plots/graphs/{title}.png", title)

        print(f'({100*progress/len(test_files): .2f}%) Graph for {test_file} has been created.')
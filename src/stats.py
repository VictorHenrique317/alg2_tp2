import os
import pandas as pd

def compare_solutions(csv_file):
    df = pd.read_csv(csv_file)

    print("Comparison of Best Solution vs Optimal Solution:")
    for index, row in df.iterrows():
        tsp_problem = row['tsp_problem']
        best_solution = row['best_solution']
        optimal_solution = row['optimal_solution']

        if pd.isna(best_solution) or pd.isna(optimal_solution):
            print(f"{tsp_problem}: Unable to compare due to missing values.")
        else:
            # Calculate the difference and percentage worse
            difference = best_solution - optimal_solution
            percentage_worse = (difference / optimal_solution) * 100

            print(f"{tsp_problem}: Best solution is {percentage_worse:.2f}% worse than the optimal solution.")

def print_nb_nodes(directory="test_data"):
    try:
        if not os.path.isdir(directory):
            print(f"Directory '{directory}' does not exist.")
            return

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)

            if os.path.isfile(filepath):
                try:
                    # Count the number of lines in the file
                    with open(filepath, 'r', encoding='utf-8') as file:
                        line_count = sum(1 for _ in file) - 7
                    print(f"{filename}: {line_count} nodes")
                except Exception as e:
                    print(f"Error reading file '{filename}': {e}")
    except Exception as e:
        print(f"Error accessing directory '{directory}': {e}")

print_nb_nodes()

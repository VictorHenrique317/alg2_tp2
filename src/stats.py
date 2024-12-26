import matplotlib.pyplot as plt
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


def plot_worse_percentage(csv_file, fig_path):
    """
    Plots a bar chart showing the values of worse_percentage for each tsp_problem.

    Args:
        csv_file (str): Path to the CSV file containing the data.
    """
    data = pd.read_csv(csv_file)

    data = data.dropna(subset=['worse_percentage'])

    data['worse_percentage'] = pd.to_numeric(data['worse_percentage'])

    plt.figure(figsize=(12, 6))
    plt.bar(data['tsp_problem'], data['worse_percentage'], color='skyblue')

    # Adding labels and title
    plt.xlabel('TSP Problem', fontsize=12)
    plt.ylabel('Worse Percentage', fontsize=12)
    plt.title('Worse Percentage for Each TSP Problem', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()
    
    plt.savefig(fig_path)
    plt.close()

def plot_worse_percentage_vs_nodes(csv_file, fig_path):
    """
    Creates a line plot of worse_percentage (y-axis) as a function of number_nodes (x-axis).
    The number of nodes will be sorted in ascending order.

    Args:
        csv_file (str): Path to the CSV file containing the data.
    """
    data = pd.read_csv(csv_file)

    data = data.dropna(subset=['worse_percentage', 'number_nodes'])

    data['worse_percentage'] = pd.to_numeric(data['worse_percentage'])
    data['number_nodes'] = pd.to_numeric(data['number_nodes'])

    data = data.sort_values(by='number_nodes')

    plt.figure(figsize=(10, 6))
    plt.plot(data['number_nodes'], data['worse_percentage'], marker='o', linestyle='-', color='blue')

    plt.xlabel('Number of Nodes', fontsize=12)
    plt.ylabel('Worse Percentage', fontsize=12)
    plt.title('Worse Percentage vs Number of Nodes', fontsize=14)

    plt.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig(fig_path)
    plt.close()

def display_top_five_worse_percentages(csv_file):
    """
    Displays the top five worse percentages and their respective TSP problems.

    Args:
        csv_file (str): Path to the CSV file containing the data.
    """
    data = pd.read_csv(csv_file)

    data = data.dropna(subset=['worse_percentage'])

    data['worse_percentage'] = pd.to_numeric(data['worse_percentage'])

    top_five = data.nlargest(5, 'worse_percentage')

    print("Top Five Worse Percentages:")
    print(top_five[['tsp_problem', 'worse_percentage']])

def display_top_five_smallest_percentages(csv_file):
    """
    Displays the top five smallest worse percentages and their respective TSP problems.

    Args:
        csv_file (str): Path to the CSV file containing the data.
    """
    data = pd.read_csv(csv_file)

    data = data.dropna(subset=['worse_percentage'])

    data['worse_percentage'] = pd.to_numeric(data['worse_percentage'])

    smallest_five = data.nsmallest(5, 'worse_percentage')

    print("Top Five Smallest Worse Percentages:")
    print(smallest_five[['tsp_problem', 'worse_percentage']])

display_top_five_smallest_percentages("results/processed/branch_and_bound.csv")

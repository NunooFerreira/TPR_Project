import pandas as pd
import matplotlib.pyplot as plt

# Function to create a scatter plot
def scatter_plot(file1, file2, metric_x, metric_y):
    # Load data from the CSV files
    data1 = pd.read_csv(file1)
    data2 = pd.read_csv(file2)

    # Check if the selected metrics are in the files
    if metric_x not in data1.columns or metric_y not in data1.columns:
        print(f"Error: '{metric_x}' or '{metric_y}' not found in {file1}")
        return
    if metric_x not in data2.columns or metric_y not in data2.columns:
        print(f"Error: '{metric_x}' or '{metric_y}' not found in {file2}")
        return

    # Create the scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(data1[metric_x], data1[metric_y], color='blue', label='File 1')
    plt.scatter(data2[metric_x], data2[metric_y], color='red', label='File 2', s=50)

    # plt.plot("")
    # Add labels, title, and legend
    plt.xlabel(metric_x)
    plt.ylabel(metric_y)
    plt.title(f"Scatter Plot of {metric_x} vs {metric_y}")
    plt.legend()

    
    # Show the plot
    plt.grid(True)
    plt.show()

# Specify the input CSV files
file1 = '../OutputedCsv/Nuno_Combined_5min_metrics.csv'  # Replace with your first CSV file
file2 = '../OutputedCsv/BOTLVL7_Combined_5min_metrics.csv'  # Replace with your second CSV file

# Specify the metrics for X and Y axes
metric_x = 'numRequests'  # Replace with the desired metric for the X-axis
metric_y = 'tamanhoResposta'  # Replace with the desired metric for the Y-axis

# Call the scatter plot function
scatter_plot(file1, file2, metric_x, metric_y)

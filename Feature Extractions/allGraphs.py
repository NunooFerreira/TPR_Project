import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations

#File to give all combiations of 2d metrics of bot and normal behaviour

# File paths
file1 = '../OutputedCsv/Nuno_Combined_5min_metrics.csv' 
file2 = '../OutputedCsv/BOTLVL8_Combined_5min_metrics.csv'  

# List of metrics to plot
metrics = ['numRequests', 'tamanhoResposta', 'totalImageSize', 'RequestsJS', 'RequestsHTML', 'RequestsCSS',
           'totalSilenceTime', 'silenceCount']

# Read the CSV files
data1 = pd.read_csv(file1)
data2 = pd.read_csv(file2)

# Check if all selected metrics are in the files
for metric in metrics:
    if metric not in data1.columns or metric not in data2.columns:
        print(f"Error: Metric '{metric}' not found in one of the files.")
        exit()

# Generate all possible combinations of metrics
metric_combinations = combinations(metrics, 2)

# Create scatter plots for each combination
for metric_x, metric_y in metric_combinations:
    plt.figure(figsize=(10, 6))
    plt.scatter(data1[metric_x], data1[metric_y], color='blue', label='File 1')
    plt.scatter(data2[metric_x], data2[metric_y], color='red', label='File 2', s=50)

    # Add labels, title, and legend
    plt.xlabel(metric_x)
    plt.ylabel(metric_y)
    plt.title(f"Scatter Plot of {metric_x} vs {metric_y}")
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()

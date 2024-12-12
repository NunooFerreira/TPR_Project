import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files
csv_blue = 'Combined_5min_metrics.csv'  # Replace with the actual filename for blue dots
csv_red = 'BOT_Combined_5min_metrics.csv'    # Replace with the actual filename for red dots

# Read data into DataFrames
df_blue = pd.read_csv(csv_blue)
df_red = pd.read_csv(csv_red)

# Choose the metrics for X and Y axes
metric_x = 'avgNumRequests'  # Replace with desired metric for X
metric_y = 'avgTamanhoResposta'  # Replace with desired metric for Y

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(df_blue[metric_x], df_blue[metric_y], color='blue', label='Blue Dots', alpha=0.7)
plt.scatter(df_red[metric_x], df_red[metric_y], color='red', label='Red Dots', alpha=0.7)

# Customize the plot
plt.title('Scatter Plot of Selected Metrics', fontsize=16)
plt.xlabel(metric_x, fontsize=14)
plt.ylabel(metric_y, fontsize=14)
plt.legend()
plt.grid(alpha=0.3)

# Show the plot
plt.tight_layout()
plt.show()

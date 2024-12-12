import pandas as pd
import matplotlib.pyplot as plt

# Function to load and process CSV files
def load_and_process_csv(file_path, metrics):
    df = pd.read_csv(file_path)
    
    # Ensure that the selected metrics exist in the DataFrame
    if not set(metrics).issubset(df.columns):
        print(f"Invalid metrics in file {file_path}. Exiting.")
        exit()
    
    # Extract the selected metrics and ensure timestamp is properly parsed
    df['timestamp'] = pd.to_datetime(df['window_start'])
    df = df[['timestamp'] + metrics]
    
    return df

# Input CSV file paths for the two datasets
csv_file1 = "Combined_5min_metrics.csv"
csv_file2 = "BOT_Combined_5min_metrics.csv"

# List available metrics (features) in the first CSV
df_sample = pd.read_csv(csv_file1)
print("Available Metrics in the CSV files:", df_sample.columns)

# Ask the user to select metrics for the N-Dimensional distribution
metrics = input("Enter comma-separated metrics you want to analyze (e.g. numRequests, tamanhoResposta, avgSilenceTime): ").split(',')
metrics = [metric.strip() for metric in metrics]

# Load and process both CSVs
df1 = load_and_process_csv(csv_file1, metrics)
df2 = load_and_process_csv(csv_file2, metrics)

# Plot the metrics over time for both datasets
plt.figure(figsize=(12, 8))

# Plot each metric for the first CSV (Blue Dots)
for metric in metrics:
    plt.plot(df1['timestamp'], df1[metric], 'bo-', label=f"{metric} (Dataset 1)", alpha=0.6)

# Plot each metric for the second CSV (Red Dots)
for metric in metrics:
    plt.plot(df2['timestamp'], df2[metric], 'ro-', label=f"{metric} (Dataset 2)", alpha=0.6)

# Add titles and labels
plt.title('Metrics Over Time (Blue and Red Dots)')
plt.xlabel('Time')
plt.ylabel('Metric Value')
plt.legend(loc='upper right')

# Show the plot
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

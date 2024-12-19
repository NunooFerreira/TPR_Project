import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Define the input CSV file
input_csv = '../OutputedCsv/Este_NunoPatriciaFinal_Combined_5min_metrics.csv'

# Load the CSV into a DataFrame
results_df = pd.read_csv(input_csv)

# Separate correlation matrices for averages and counts
avg_columns = [col for col in results_df.columns if col.startswith('avg')]
count_columns = ['numRequests', 'tamanhoResposta', 'totalImageSize', 'RequestsJS', 'RequestsHTML', 'RequestsCSS', 'silenceCount', 'totalSilenceTime']

# Correlation for counts
count_corr_matrix = results_df[count_columns].corr()

# Set a correlation threshold (e.g., 0.8)
threshold = 0.8

# Create a list of features to drop based on high correlation
features_to_drop = set()

# Iterate over the upper triangle of the correlation matrix to find highly correlated pairs
for i in range(len(count_corr_matrix.columns)):
    for j in range(i):
        if abs(count_corr_matrix.iloc[i, j]) > threshold:
            colname = count_corr_matrix.columns[i]
            dropped_colname = count_corr_matrix.columns[j]
            # Add to the set of features to drop
            features_to_drop.add(dropped_colname)
            print(f"Drop {dropped_colname} because it is highly correlated with {colname}")

# Print the features to keep
features_to_keep = [col for col in count_columns if col not in features_to_drop]
print("\nFeatures to keep based on the correlation threshold:", features_to_keep)

# Mask the upper triangle of the matrix (excluding the diagonal)
mask = np.triu(np.ones_like(count_corr_matrix, dtype=bool), k=1)

# Plot the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(count_corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, mask=mask)
plt.title("Correlation Matrix")
plt.xticks(rotation=360, fontsize=10)
plt.yticks(fontsize=10)
plt.show()

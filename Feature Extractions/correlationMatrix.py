import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Define the input CSV file
input_csv = '../OutputedCsv/Nuno_PatriciaLogs.csv'

# Load the CSV into a DataFrame
results_df = pd.read_csv(input_csv)

# Separate correlation matrices for averages and counts
avg_columns = [col for col in results_df.columns if col.startswith('avg')]
count_columns = ['numRequests', 'tamanhoResposta', 'totalImageSize', 'RequestsJS', 'RequestsHTML', 'RequestsCSS', 'silenceCount', 'totalSilenceTime']

# Correlation for counts
count_corr_matrix = results_df[count_columns].corr()

# Mask the upper triangle of the matrix (excluding the diagonal)
mask = np.triu(np.ones_like(count_corr_matrix, dtype=bool), k=1)

plt.figure(figsize=(10, 8))
sns.heatmap(count_corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, mask=mask)
plt.title("Correlation Matrix - Count Metrics")
plt.xticks(rotation=360, fontsize=10)
plt.yticks(fontsize=10)
plt.show()

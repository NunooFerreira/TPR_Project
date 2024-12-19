import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore


good_data = pd.read_csv("good_data.csv")
bad_data = pd.read_csv("bad_data_8.csv")

# Assuming both datasets have the same columns
columns = [ "avgNumRequests", "avgTamanhoResposta", "avgTotalImageSize", "avgRequestsJS", "avgRequestsHTML", 
           "avgRequestsCSS","avgSilenceTime", "silenceCount"]

# Combine the datasets for comparison
combined_data = pd.concat([good_data, bad_data], axis=0, ignore_index=True)
combined_data['Label'] = [0] * len(good_data) + [1] * len(bad_data)  # Add label for good (0) and bad (1)

# Calculate Z-scores for each column
z_scores = combined_data[columns].apply(zscore, axis=0)

# Adjusting the figure size and number of subplots
fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(18, 10))  # Increase figure size and set grid layout
axes = axes.flatten()  # Flatten the 2D array of axes for easier indexing

# Plot the Z-scores for good and bad data
for i, column in enumerate(columns):
    good_column = z_scores.iloc[:len(good_data), i]
    bad_column = z_scores.iloc[len(good_data):, i]

    axes[i].hist(good_column, bins=30, alpha=0.7, label='Dataset Bom', color='g')
    axes[i].hist(bad_column, bins=30, alpha=0.7, label='DataSet do Bot Lvl 8', color='r')
    axes[i].set_title(f'{column}')
    axes[i].legend()



plt.tight_layout()  
plt.show()

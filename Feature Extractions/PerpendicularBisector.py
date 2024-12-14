import pandas as pd
import matplotlib.pyplot as plt

# Load the good and bad datasets
good_file = 'Nuno_Combined_5min_metrics.csv'
bad_file = 'BOTLVL2_Combined_5min_metrics.csv'

good_df = pd.read_csv(good_file)
bad_df = pd.read_csv(bad_file)

# Extract metrics of interest
# X-axis: numRequests, Y-axis: avgTamanhoResposta
good_df['label'] = 'good'
bad_df['label'] = 'bad'

data = pd.concat([good_df, bad_df], ignore_index=True)

# Compute centroids
good_centroid = good_df[['numRequests', 'avgTamanhoResposta']].mean()
bad_centroid = bad_df[['numRequests', 'avgTamanhoResposta']].mean()

# Compute the line connecting centroids
slope = (bad_centroid['avgTamanhoResposta'] - good_centroid['avgTamanhoResposta']) / (bad_centroid['numRequests'] - good_centroid['numRequests'])
intercept = good_centroid['avgTamanhoResposta'] - slope * good_centroid['numRequests']

# Compute the perpendicular bisector
perp_slope = -1 / slope
midpoint = {
    'x': (good_centroid['numRequests'] + bad_centroid['numRequests']) / 2,
    'y': (good_centroid['avgTamanhoResposta'] + bad_centroid['avgTamanhoResposta']) / 2
}
bisector_intercept = midpoint['y'] - perp_slope * midpoint['x']

# Plot the results
plt.figure(figsize=(10, 6))

# Scatter plot for good and bad data
plt.scatter(good_df['numRequests'], good_df['avgTamanhoResposta'], color='blue', label='Good (Legitimate)', alpha=0.7)
plt.scatter(bad_df['numRequests'], bad_df['avgTamanhoResposta'], color='red', label='Bad (Attack)', alpha=0.7)

# Plot centroids
plt.scatter(good_centroid['numRequests'], good_centroid['avgTamanhoResposta'], color='cyan', label='Good Centroid', s=100)
plt.scatter(bad_centroid['numRequests'], bad_centroid['avgTamanhoResposta'], color='orange', label='Bad Centroid', s=100)

# Plot the line connecting centroids
x_vals = range(int(data['numRequests'].min()), int(data['numRequests'].max()) + 1)
line_y_vals = [slope * x + intercept for x in x_vals]
plt.plot(x_vals, line_y_vals, label='Line Connecting Centroids', color='gray', linestyle='--')

# Plot the perpendicular bisector
bisector_y_vals = [perp_slope * x + bisector_intercept for x in x_vals]
plt.plot(x_vals, bisector_y_vals, label='Perpendicular Bisector', color='green')

# Add labels and legend
plt.xlabel('Number of Requests (numRequests)')
plt.ylabel('Average Response Size (avgTamanhoResposta)')
plt.title('Good vs Bad Traffic with Perpendicular Bisector')
plt.legend()
plt.grid(True)
plt.show()

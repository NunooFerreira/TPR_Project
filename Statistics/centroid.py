import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report

# Good traffic, label = 0
# Bad traffic, label = 1

# Mudar aqui para fazer centroid csv.
csv_file = "centroid_1_to_6.csv"     
df = pd.read_csv(csv_file)

# Exclude the Label column from normalization
columns_to_normalize = [col for col in df.columns if col != "Label"]

# Aplicar o Min-Max Scaling dos slides do stor o 2 ponto.
for column in columns_to_normalize:
    min_val = df[column].min()
    max_val = df[column].max()
    df[column] = (df[column] - min_val) / (max_val - min_val)

# Save the normalized dataset
output_csv = "../OutputedCsv/normalized_file.csv"  
df.to_csv(output_csv, index=False)
print(f"Normalized dataset saved to {output_csv}")

# Select columns 1 to 6, 13, and 15 
columns_to_select = list(range(0, 6)) + [12, 14, 15]

# Filter rows where the 'Label' column is 0 (assuming 'Label' is in the original df)
filtered_df = df[df['Label'] == 0]
df_good = filtered_df.iloc[:, columns_to_select]

# Filter rows where the 'Label' column is 1 (assuming 'Label' is in the original df)
filtered_df = df[df['Label'] == 1]
df_bad = filtered_df.iloc[:, columns_to_select]

# Split training and testing datasets
df_train = df_good[:76]  # Train dataset: first 70% of the good data
df_test = pd.concat([df_good[76:], df_bad], ignore_index=True)  # Test dataset: remaining 30% of the good data + 100% of the bad data

df_test_good = df_good[76:]
df_test_bad = df_bad

# Compute the centroid of df_train excluding column 15 (label)  Apenas usamos 2 metricas para ser mais simples
columns_for_centroid = ["numRequests", "tamanhoResposta"]  # Metrics to use
centroid = df_train[columns_for_centroid].mean()
print("Centroid of the training dataset (excluding Label column):")
print(centroid)

# Calculate the largest Euclidean distance to the centroid
def euclidean_distance(row, centroid):
    return np.sqrt(((row - centroid) ** 2).sum())

distances = df_train[columns_for_centroid].apply(lambda row: euclidean_distance(row, centroid), axis=1)
max_distance = distances.max()
print("Largest Euclidean distance to the centroid:", max_distance)

# Determine the radius using the interquartile range (IQR)  Quartil 1 e 3 foi o melhor resultado.
q1, q3 = np.percentile(distances, [25, 75])
iqr = q3 - q1
k = 1.0
radius = np.median(distances) + k * iqr

# Extract centroid coordinates
x_centroid, y_centroid = centroid["numRequests"], centroid["tamanhoResposta"]

# Generate points for the circumference
theta = np.linspace(0, 2 * np.pi, 100)  # 100 points around the circle
x_circle = x_centroid + radius * np.cos(theta)
y_circle = y_centroid + radius * np.sin(theta)

# Ensure no negative values for x and y coordinates of the circle
x_circle = np.where(x_circle < 0, 0, x_circle)
y_circle = np.where(y_circle < 0, 0, y_circle)

# Count the number of bad points (red dots) inside the radius
df_test_bad["distance_to_centroid"] = df_test_bad[columns_for_centroid].apply(
    lambda row: euclidean_distance(row, centroid), axis=1
)
red_dots_inside = df_test_bad[df_test_bad["distance_to_centroid"] <= radius].shape[0]
print(f"Number of red dots (bad data) inside the radius: {red_dots_inside}")

# Plot the circumference and training data
fig1 = plt.figure(figsize=(8, 8))
ax = plt.axes()
ax.plot(x_circle, y_circle, label="Circumference (radius={:.2f})".format(radius), color="blue")
ax.scatter(df_train["numRequests"], df_train["tamanhoResposta"], label="Training Data", color="green")
ax.scatter(x_centroid, y_centroid, color="black", label="Centroid", zorder=5)
ax.set_xlabel("numRequests")
ax.set_ylabel("tamanhoResposta")
ax.set_title("Circumference around Centroid With Training Data Bot 1-8")
ax.legend()
ax.grid(True)
ax.axis("equal")  # Equal scaling for x and y axes

# Plot the circumference and testing data
fig2 = plt.figure(figsize=(8, 8))
ax = plt.axes()
ax.plot(x_circle, y_circle, label="Circumference (radius={:.2f})".format(radius), color="blue")
ax.scatter(df_test_good["numRequests"], df_test_good["tamanhoResposta"], label="Good Data", color="green")
ax.scatter(df_test_bad["numRequests"], df_test_bad["tamanhoResposta"], label="Bad Data", color="red")
ax.scatter(x_centroid, y_centroid, color="black", label="Centroid", zorder=5)
ax.set_xlabel("numRequests")
ax.set_ylabel("tamanhoResposta")
ax.set_title("Circumference around Centroid With Testing Data Bot 1-8")
ax.legend()
ax.grid(True)
ax.axis("equal")  # Equal scaling for x and y axes
plt.show()

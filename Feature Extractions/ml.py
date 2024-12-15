import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report


csv_file = "LOGS_TOTAL.csv"  
df = pd.read_csv(csv_file)

# Exclude the Label column from normalization
columns_to_normalize = [col for col in df.columns if col != "Label"]

# Apply Min-Max Scaling
for column in columns_to_normalize:
    min_val = df[column].min()
    max_val = df[column].max()
    df[column] = (df[column] - min_val) / (max_val - min_val)

# Save the normalized dataset
output_csv = "../OutputedCsv/normalized_file.csv"  
df.to_csv(output_csv, index=False)
print(f"Normalized dataset saved to {output_csv}")

# Select columns 1 to 6, 13, and 15 (Python uses zero-based indexing, so adjust accordingly)
columns_to_select = list(range(0, 6)) + [12, 14, 15]

# Filter rows where the 'Label' column is 0 (assuming 'Label' is in the original df)
filtered_df = df[df['Label'] == 0]
df_good = filtered_df.iloc[:, columns_to_select]


# Filter rows where the 'Label' column is 0 (assuming 'Label' is in the original df)
filtered_df = df[df['Label'] == 1]
df_bad = filtered_df.iloc[:, columns_to_select] 


df_train = df_good[:76] # Train dataset os primeiros 70% dos bons
df_test = pd.concat([df_good[76:] , df_bad], ignore_index=True) #Test dataset com o resto dos 30% dos bons + 100% dos maus
df_test_good = df_good[76:]
df_test_bad = df_bad

# Compute the centroid of df_train excluding column 15 (label)
columns_for_centroid = ["numRequests", "tamanhoResposta"]       #Mudar aqui para escolher as metricas
centroid = df_train[columns_for_centroid].mean()
print("Centroid of the training dataset (excluding Label column):")
print(centroid)

# Calculate the largest Euclidean distance to the centroid
def euclidean_distance(row, centroid):
    return np.sqrt(((row - centroid) ** 2).sum())

distances = df_train[columns_for_centroid].apply(lambda row: euclidean_distance(row, centroid), axis=1)
max_distance = distances.max()
print("Largest Euclidean distance to the centroid:", max_distance)

#threshold = 0
#radius = max_distance + threshold
q1, q3 = np.percentile(distances, [25,75])
iqr = q3 - q1
k = 1.2
radius = np.median(distances) + k*iqr

# Extract centroid coordinates
x_centroid, y_centroid = centroid["numRequests"], centroid["tamanhoResposta"]

# Generate points for the circumference
theta = np.linspace(0, 2 * np.pi, 100)  # 100 points around the circle
x_circle = x_centroid + radius * np.cos(theta)
y_circle = y_centroid + radius * np.sin(theta)

# Ensure no negative values for x and y coordinates of the circle
x_circle = np.where(x_circle < 0, 0, x_circle)
y_circle = np.where(y_circle < 0, 0, y_circle)


# Plot the circumference and training data
fig1 = plt.figure(figsize=(8, 8))
ax = plt.axes()
ax.plot(x_circle, y_circle, label="Circumference (radius={:.2f})".format(radius), color="blue")
ax.scatter(df_train["numRequests"], df_train["tamanhoResposta"], label="Training Data", color="green")
ax.scatter(x_centroid, y_centroid, color="black", label="Centroid", zorder=5)
ax.set_xlabel("numRequests")
ax.set_ylabel("tamanhoResposta")
ax.set_title("Circumference around Centroid With Traning Data")
ax.legend()
ax.grid(True)
ax.axis("equal")  # Equal scaling for x and y axes


# Plot the circumference and training data
fig2 = plt.figure(figsize=(8, 8))
ax = plt.axes()
ax.plot(x_circle, y_circle, label="Circumference (radius={:.2f})".format(radius), color="blue")
ax.scatter(df_test_good["numRequests"], df_test_good["tamanhoResposta"], label="Testing Data", color="green")
ax.scatter(df_test_bad["numRequests"], df_test_bad["tamanhoResposta"], label="Testing Data", color="red")
ax.scatter(x_centroid, y_centroid, color="black", label="Centroid", zorder=5)
ax.set_xlabel("numRequests")
ax.set_ylabel("tamanhoResposta")
ax.set_title("Circumference around Centroid With Testing Data")
ax.legend()
ax.grid(True)
ax.axis("equal")  # Equal scaling for x and y axes
plt.show()


# Confusion Matrix:
from sklearn.metrics import confusion_matrix, classification_report

# Combine testing data
df_test["numRequests"] = df_test["numRequests"].astype(float)
df_test["tamanhoResposta"] = df_test["tamanhoResposta"].astype(float)

# Compute the Euclidean distance for each test sample
df_test["distance_to_centroid"] = df_test[columns_for_centroid].apply(
    lambda row: euclidean_distance(row, centroid), axis=1
)

# Classify based on distance to centroid
df_test["predicted_label"] = df_test["distance_to_centroid"].apply(
    lambda dist: 0 if dist <= radius else 1
)

# Extract actual labels
actual_labels = df_test["Label"]
predicted_labels = df_test["predicted_label"]

# Compute confusion matrix
conf_matrix = confusion_matrix(actual_labels, predicted_labels)

# Print confusion matrix and classification report
print("Confusion Matrix:")
print(conf_matrix)

print("\nClassification Report:")
print(classification_report(actual_labels, predicted_labels))

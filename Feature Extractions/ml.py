import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

# Load the dataset
file = 'LOGS_TOTAL.csv'
df = pd.read_csv(file)

# Select features and labels
X = df[['numRequests', 'avgTamanhoResposta']]  # Features
y = df['Label']  # Labels

# Normalize the data (optional)
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Split the data based on structure
good_data = X_scaled[:109]  # First 109 rows are good traffic
bad_data = X_scaled[109:]  # Rows from 109 onward are bad traffic

# 70% good traffic for training
train_size = int(0.7 * len(good_data))
train_good = good_data[:train_size]
test_good = good_data[train_size:]

# Centroid calculation using training data
centroid = np.mean(train_good, axis=0)

# Testing data: 30% good + all bad traffic
test_data = np.vstack([test_good, bad_data])
test_labels = np.hstack([np.zeros(len(test_good)), np.ones(len(bad_data))])  # 0: good, 1: bad

# Calculate distances to the centroid
distances = np.linalg.norm(test_data - centroid, axis=1)

# Set a threshold for anomaly detection
threshold = np.percentile(np.linalg.norm(train_good - centroid, axis=1), 95)  # 95th percentile of good distances
predictions = (distances > threshold).astype(int)  # 0: normal, 1: anomaly

# Evaluate
print("Confusion Matrix:")
print(confusion_matrix(test_labels, predictions))
print("\nClassification Report:")
print(classification_report(test_labels, predictions, target_names=['Good', 'Anomaly']))

# Visualization
plt.scatter(test_good[:, 0], test_good[:, 1], label='Good Traffic (Test)', alpha=0.5, c='blue')
plt.scatter(bad_data[:, 0], bad_data[:, 1], label='Bad Traffic (Test)', alpha=0.5, c='red')
plt.scatter(centroid[0], centroid[1], label='Centroid', c='green', marker='x', s=100)
circle = plt.Circle(centroid, threshold, color='green', fill=False, linestyle='--', label='Threshold Boundary')
plt.gca().add_artist(circle)
plt.title("Traffic Data with Centroid-Based Anomaly Detection")
plt.xlabel("numRequests (Normalized)")
plt.ylabel("avgTamanhoResposta (Normalized)")
plt.legend()
plt.show()

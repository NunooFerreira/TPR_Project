import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from matplotlib.colors import ListedColormap

# Load the dataset
data = pd.read_csv('All_with_7_8.csv')

# Features (metrics) and Labels
X = data.drop('Label', axis=1)  # All features except 'Label'
y = data['Label']  # Labels (good = 0, bad = 1)

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Apply PCA to reduce the dimensions to 2D for visualization 
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

# Define the SVM classifier with a linear kernel
# model = SVC(kernel='linear')
model = SVC(kernel='linear')
# model = SVC(kernel='poly', degree=3)
#rbf

model.fit(X_train_pca, y_train)

# Create a mesh grid to plot decision boundaries
h = .02  # Step size in the mesh
x_min, x_max = X_train_pca[:, 0].min() - 1, X_train_pca[:, 0].max() + 1
y_min, y_max = X_train_pca[:, 1].min() - 1, X_train_pca[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

# Predict using the model to get decision boundaries
Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)



        #APenas codigo de plots apra ficar com as cores do slides do stor:

# Plot the decision boundary and the training points
custom_cmap = ListedColormap(['#4678AB', '#B04152'])  # Light Blue, Light Pink
plt.contourf(xx, yy, Z, alpha=0.8, cmap=custom_cmap)
plt.scatter(X_train_pca[:, 0], X_train_pca[:, 1], 
            c=y_train, edgecolors='k', cmap=custom_cmap, s=50)

# Label the plot
plt.title("SVM with linear kernel (Reduced to 2D)")
plt.xlabel("numRequests") 
plt.ylabel("tamanhoResposta")  
plt.show()

# Predict on the test data
y_pred = model.predict(X_test_pca)

# Compute the confusion matrix
cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
print(cm)

# Display the confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Good Data (0)", "Bad Data (1)"])
disp.plot(cmap='Blues', values_format='d')
plt.title("Confusion Matrix")
plt.show()

accuracy = np.trace(cm) / np.sum(cm)
print(f"Overall Accuracy: {accuracy:.2f}")
print(classification_report(y_test, y_pred))

from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.discriminant_analysis import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
from sklearn.gaussian_process.kernels import RBF, ConstantKernel  # Import ConstantKernel explicitly

#Aqui depende se queremos os mais inteligentes ou do 1_8 que da piores resultados com utilizadores bonns a serem bloqueados
data = pd.read_csv('All_with_7_8.csv')

# Features (metrics) and Labels
X = data.drop('Label', axis=1)  # Features (metrics)
y = data['Label']  # Labels (good = 0, bad = 1)

X_2d = X[['numRequests', 'tamanhoResposta']]  # Select 2D features for visualization

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_2d, y, test_size=0.3, random_state=44)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=44, max_depth=5, class_weight='balanced')  # Adjust max_depth and n_estimators as needed
model.fit(X_train_scaled, y_train)

# Create a mesh grid to plot decision boundaries
h = .02  # Step size in the mesh
x_min, x_max = X_train_scaled[:, 0].min() - 1, X_train_scaled[:, 0].max() + 1
y_min, y_max = X_train_scaled[:, 1].min() - 1, X_train_scaled[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

# Predict using the model to get decision boundaries
Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)


        #APenas codigo de plots apra ficar com as cores do slides do stor:

# Just for background color
custom_cmap = ListedColormap(['#4678AB', '#B04152'])  # Light Blue, Light Pink

# Plotting
plt.contourf(xx, yy, Z, alpha=0.8, cmap=custom_cmap)
plt.scatter(X_train_scaled[:, 0], X_train_scaled[:, 1], 
            c=y_train, edgecolors='k', cmap=custom_cmap, s=50)

# Label the plot
plt.title("Random Forest Classifier (2D features)")
plt.xlabel("numRequests")
plt.ylabel("tamanhoResposta")
plt.show()

# Predict on the test data
y_pred = model.predict(X_test_scaled)

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

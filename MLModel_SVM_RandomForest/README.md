# Machine Learning

## Overview

This directory contains the machine learning scripts and resources used to classify legitimate and malicious traffic in the DDoS Layer 7 project. The models focus on distinguishing normal user behavior from bot-generated traffic based on features extracted from the dataset. The directory includes implementations of two machine learning models: Random Forest Classifier and Support Vector Machine (SVM).

---

## Files and Descriptions

### 1. `random_forest_model.py`

- Implements a Random Forest Classifier to classify traffic into legitimate (good data) and malicious (bad data).
- **Key Features**:
  - Utilizes `numRequests` and `tamanhoResposta` as 2D features for visualization.
  - Standardizes features using `StandardScaler`.
  - Visualizes decision boundaries with a custom colormap.
  - Computes and displays a confusion matrix for performance evaluation.
  - Outputs accuracy and a classification report.
- **Usage**:
  - Load dataset: `All_with_7_8.csv`
  - Train-test split: 70% training, 30% testing.

### 2. `svm_model.py`

- Implements an SVM Classifier with dimensionality reduction via PCA for visualization.
- **Key Features**:
  - Reduces features to 2D using Principal Component Analysis (PCA).
  - Tests with a linear kernel (configurable for other kernels).
  - Visualizes decision boundaries with a custom colormap.
  - Computes and displays a confusion matrix for performance evaluation.
  - Outputs accuracy and a classification report.
- **Usage**:
  - Load dataset: `All_with_7_8.csv`
  - Train-test split: 70% training, 30% testing.

### 3. `All_with_7_8.csv`

- Combined dataset of normal user traffic and bot-generated traffic.
- **Structure**:
  - Contains extracted features such as `numRequests`, `tamanhoResposta`, `RequestsJS`, `RequestsHTML`, `RequestsCSS`, etc.
  - Includes a `Label` column with binary values:
    - `0` for legitimate traffic.
    - `1` for malicious traffic.
- **Purpose**:
  - Used as the primary dataset for training and testing models.

---

## Requirements

- **Libraries**:
  - `matplotlib`
  - `pandas`
  - `numpy`
  - `scikit-learn`

---

## How to Run

1. **Prepare Environment**:
   - Ensure Python and required libraries are installed.
   - Place the `All_with_7_8.csv` file in the same directory as the scripts.

2. **Random Forest Classifier**:
   - Execute `random_forest_model.py`.
   - Observe decision boundaries and performance metrics.

3. **SVM Classifier**:
   - Execute `svm_model.py`.
   - Observe decision boundaries and performance metrics.

---

## Outputs

1. **Visualizations**:
   - Decision boundary plots for both models.
   - Confusion matrices with detailed metrics.

2. **Performance Metrics**:
   - Accuracy score.
   - Precision, recall, and F1-score via classification reports.

---

## Notes

- Ensure `All_with_7_8.csv` is properly formatted and includes all necessary features and labels.
- Customize hyperparameters (e.g., `n_estimators` for Random Forest, `kernel` for SVM) as needed for better performance.

## Results

- SVM Using Linear Kernel:

![svmlinear](https://github.com/user-attachments/assets/ffefebff-392b-4b21-a7c8-5ae8f3bca0b6)

![svmconfusionon](https://github.com/user-attachments/assets/dc217969-65bd-4647-8dd9-74bd4a9bc546)

![svmresults](https://github.com/user-attachments/assets/10dc22e8-46a6-42bb-8273-4553f0c90cfd)



- Random Forest

![randomforest](https://github.com/user-attachments/assets/57c63da6-7538-4f24-a68f-ca57fff39d49)

![confusinmatreixrandom](https://github.com/user-attachments/assets/9524cb91-86d0-48b3-8b35-e6113c134aab)

![randomforestresults](https://github.com/user-attachments/assets/deb0f5da-45f3-4e02-aeea-156276fe2417)

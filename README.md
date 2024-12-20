# DDoS Layer 7 Attack and Defense Project

## Overview

This project demonstrates the detection and mitigation of DDoS (Distributed Denial-of-Service) Layer 7 attacks. These attacks target the application layer of the OSI model and are designed to mimic legitimate user traffic, making detection challenging. The work involves creating a vulnerable web environment, simulating both normal and malicious traffic, extracting metrics for analysis, and implementing machine learning-based anomaly detection to identify and defend against such attacks.

---

## Features

1. **Website and Environment Setup**:
   - Developed a website hosted on an Apache2 server.
   - Collected web server logs capturing interactions from both legitimate users and bots.

2. **Attack Simulation**:
   - Created bots using Python libraries (`requests` and `BeautifulSoup`) to simulate malicious behavior.
   - Designed 8 levels of bots with varying attack patterns (e.g., fixed intervals, random intervals, Gaussian-distributed intervals).

3. **Metrics and Features Extraction**:
   - Extracted key metrics from Apache2 access logs:
     - **Metrics per 30-second sub-window**:
       - `numRequests`, `tamanhoResposta`, `totalImageSize`, `RequestsJS`, `RequestsHTML`, `RequestsCSS`, `totalSilenceTime`, `silenceCount`.
     - **Aggregated Features for 5-minute windows**:
       - Average values of metrics above.

4. **Data Processing and Analysis**:
   - Implemented time windowing techniques with sliding windows (1-minute increments).
   - Applied statistical methods (e.g., Z-Score) and feature scaling for anomaly detection.

5. **Anomaly Detection**:
   - Used centroid-based classification and interquartile range (IQR) for detecting deviations in feature patterns.
   - Employed Support Vector Machines (SVM) with different kernels and class balancing techniques for bot detection.

6. **Performance**:
   - Detected bots across all levels (1-8) with high accuracy.
   - Achieved 95% precision with the best machine learning model.

---

## Requirements

- **Server**: Apache2 web server
- **Languages**: Python (for bots and data processing)
- **Libraries**:
  - `requests`, `BeautifulSoup` for bot creation
  - Machine learning libraries such as `scikit-learn`

---

## Structure

### Dataset

- **Normal Traffic**: Generated by simulating interactions of legitimate users.
- **Malicious Traffic**: Generated by bots executing repetitive and complex Layer 7 attacks.

### Training and Testing

- Training dataset: 70% of the collected data.
- Testing dataset: 30% of the collected data.

### Output

- Features and metrics are saved in CSV format for analysis.
- Anomaly detection results are visualized and summarized in performance reports.

---

## How to Run

1. **Setup Environment**:
   - Install Apache2 and configure the website.
   - Clone the repository and ensure Python dependencies are installed.

2. **Generate Data**:
   - Run scripts to simulate normal and malicious traffic.
   - Collect and preprocess Apache2 access logs.

3. **Feature Extraction**:
   - Use the provided Python scripts to calculate metrics and aggregate features.

4. **Anomaly Detection**:
   - Run the machine learning models (SVM and Random Forest) with the prepared datasets.

5. **Evaluation**:
   - Analyze detection results and visualize feature evolution over time.

---

## Authors

- Nuno Ferreira
- Patricia Cardoso

## License

This project is for educational purposes and should not be used maliciously.


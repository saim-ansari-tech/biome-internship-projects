# Biome Internship Projects

This repository contains the tasks and projects completed during my internship at **Biome**. Each task focuses on a different aspect of data analysis, data quality, and machine learning operations (MLOps), with an emphasis on writing clean, modular, and production-oriented Python code.

---

## Repository Structure

```text
biome-internship-projects/
│
├── .github/
│   └── workflows/
│       └── flake8.yaml
│
├── README.md
│
├── Task1/
│   ├── data/
│   ├── notebook/
│   ├── src/
│   └── requirements.txt
│
├── Task2/
│   ├── data/
│   ├── src/
│   └── requirements.txt
│
└── Task3/
    ├── data/
    ├── src/
    └── requirements.txt
```

---

# Tasks Overview

## Task 1 – Weather Data Profiling

### Objective

Perform comprehensive data profiling on a weather dataset to understand its statistical properties, data quality, and feature distributions through descriptive statistics and visualizations.

### Features

* Dataset overview
* Data type inspection
* Missing value analysis
* Descriptive statistics for numerical features:

  * Mean
  * Median
  * Minimum
  * Maximum
  * First Quartile (Q1)
  * Third Quartile (Q3)
* Mode calculation for categorical features
* Numerical feature visualization
* Correlation analysis
* Modular and reusable profiling pipeline

### Technologies

* Python
* Pandas
* Matplotlib
* Seaborn

---

## Task 2 – Data Drift Detection Using Population Stability Index (PSI)

### Objective

Detect distribution changes between a baseline dataset and a new dataset using the **Population Stability Index (PSI)** implemented **from scratch** without relying on external drift detection libraries.

### Features

* Custom PSI implementation
* Numerical feature comparison
* Distribution visualization
* PSI calculation for each numerical feature
* Automated drift report generation

### Drift Interpretation

|         PSI Score | Interpretation    |
| ----------------: | ----------------- |
|        PSI < 0.10 | No Drift          |
| 0.10 ≤ PSI < 0.25 | Moderate Drift    |
|        PSI ≥ 0.25 | Significant Drift |

### Technologies

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn

---

## Task 3 – Weighted Data Rebalancing Strategy

### Objective

Simulate a real-world production scenario where a machine learning model is trained on historical data, but the incoming production data experiences significant distribution drift.

To address this problem, a weighted data combination strategy was implemented.

### Strategy

The algorithm combines:

* **30%** of the original (training) dataset
* **70%** of the drifted (production) dataset

The resulting dataset provides a smoother transition toward the new production distribution while preserving information from the original data.

### Features

* Load original dataset
* Load drifted dataset
* Apply configurable weighted sampling
* Generate a new combined dataset
* Export the final dataset as a CSV file

### Output

The generated CSV can be used for:

* Model retraining
* Continuous learning pipelines
* Dataset rebalancing
* Production model updates

---

# Code Quality

This repository follows Python coding best practices and includes automated code quality checks using **Flake8**.

GitHub Actions automatically runs linting on every push through the workflow located at:

```text
.github/workflows/flake8.yaml
```

---

# Requirements

Each task contains its own `requirements.txt` file containing the required Python dependencies.

Install the dependencies for a task using:

```bash
pip install -r requirements.txt
```

---

# Skills Demonstrated

* Python Programming
* Data Profiling
* Exploratory Data Analysis (EDA)
* Data Visualization
* Population Stability Index (PSI)
* Data Drift Detection
* Machine Learning Data Monitoring
* Dataset Rebalancing
* MLOps Concepts
* Git & GitHub
* GitHub Actions
* Flake8
* Modular Project Structure

---

# Internship

This repository serves as a collection of projects completed during my internship at **Biome**, demonstrating practical applications of data analysis, data quality assessment, and production-oriented machine learning workflows.

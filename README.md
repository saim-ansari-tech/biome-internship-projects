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

## Task 4 - Predict 30-day readmission risk and identify actionable drivers

# Diabetes 130-US Hospitals: 30-Day Readmission Risk Prediction

A production-style machine learning pipeline that predicts whether a diabetic patient will be readmitted to the hospital within 30 days, built on the UCI Diabetes 130-US Hospitals dataset. The project covers the full lifecycle: data cleaning, feature engineering, encoding, model training, handling class imbalance, and model explainability with SHAP.

## Objective

Hospital readmissions within 30 days are a key quality and cost metric for healthcare providers. This project frames the problem as a binary classification task: predict whether a patient will be readmitted within 30 days (`1`) or not (`0`), using structured clinical and administrative data collected during a hospital encounter.

## Dataset

- **Source:** UCI Diabetes 130-US Hospitals dataset
- **Target column:** `readmitted`
- **Target transformation:**
  - `<30` → `1` (readmitted within 30 days)
  - `>30` or `NO` → `0`

## Pipeline Overview

### 1. Data Loading
Raw data loaded from CSV using pandas.

### 2. Preprocessing
- Replaced placeholder values (`?`) with proper missing values.
- Dropped non-informative or leakage-prone identifier columns: `encounter_id`, `patient_nbr`, `weight`.
- Removed invalid or terminal records:
  - Rows where `gender == "Unknown/Invalid"`
  - Rows where `discharge_disposition_id` indicates the patient expired (`11`, `19`, `20`)
- Converted categorical ID columns (`admission_type_id`, `discharge_disposition_id`, `admission_source_id`) into meaningful categories.
- Imputed missing values: `payer_code`, `medical_specialty`, and `race` filled with `"Unknown"`.
- Grouped rare/low-frequency categories in `medical_specialty`, `payer_code`, and `admission_source_id` to reduce dimensionality and noise.

### 3. Feature Engineering
New features created to capture clinical severity and utilization patterns:
- `total_visits`: aggregate of prior outpatient, inpatient, and emergency visits.
- `long_stay`: binary flag based on the 75th percentile of `time_in_hospital`.
- `high_medications`: binary flag based on the 75th percentile of `num_medications`.
- `multiple_diagnoses`: binary flag based on the 75th percentile of `number_diagnoses`.
- Diagnosis grouping for `diag_1`, `diag_2`, and `diag_3` into clinically meaningful categories (e.g., Circulatory, Diabetes, Respiratory).

### 4. Encoding
- **Binary encoding:** `gender`, `change`, `diabetesMed`
- **One-hot encoding:** `race`, `admission_type_id`, `discharge_disposition_id`, `admission_source_id`, `payer_code`, `medical_specialty`, diagnosis groups, medication columns, `max_glu_serum`, `A1Cresult`

### 5. Modeling
- **Split:** `train_test_split` with stratification on the target to preserve class ratio.
- **Scaling:** `StandardScaler` applied only for Logistic Regression, fit on training data and applied to test data. Tree-based models were left unscaled.
- **Models trained:**
  - Logistic Regression (baseline, interpretable)
  - Random Forest
  - XGBoost
- **Evaluation metrics:** Accuracy, Precision, Recall, F1-score, full classification report, and confusion matrix.

### 6. Handling Class Imbalance
Initial models showed poor recall on the minority (readmitted) class. Addressed using class balancing techniques (`class_weight` for Logistic Regression/Random Forest, `scale_pos_weight` for XGBoost) to improve minority class detection, since missing a true readmission is more costly than a false alarm in this domain.

### 7. Explainability (SHAP)
Used SHAP with the XGBoost model to interpret predictions at both global and local levels:
- Global feature importance (bar plot)
- Beeswarm plot for feature impact distribution

**Top contributing features:**
- `number_inpatient`
- `discharge_disposition_id_1`
- `number_diagnoses`
- `num_medications`
- `total_visits`
- `num_lab_procedures`
- `age`
- `diag_1_group_Circulatory`
- `time_in_hospital`

## Project Structure

```
src/
├── preprocessing.py       # Data cleaning and missing value handling
├── feature_engineering.py # Derived feature creation
├── encoding.py             # Binary and one-hot encoding logic
├── model.py                # Model training and evaluation
└── main.py                  # Pipeline entry point
```

## Key Lessons

- Never scale data before the train/test split, scaling on the full dataset leaks test information into training.
- Fit the scaler only on training data, then transform the test set with the same scaler.
- Tree-based models (Random Forest, XGBoost) do not require feature scaling.
- Accuracy alone is a misleading metric on imbalanced datasets like this one.
- Recall and F1-score matter more than accuracy here, since failing to flag a high-risk readmission has real clinical cost.
- SHAP is an effective tool for turning a black-box model into something clinically interpretable, which matters for trust and adoption in healthcare settings.

## Tech Stack

- **Language:** Python
- **Core libraries:** pandas, numpy, scikit-learn, XGBoost
- **Explainability:** SHAP
- **Visualization:** matplotlib / seaborn (for evaluation and SHAP plots)

## How to Run

```bash
# Clone the repository
git clone <repo-url>
cd <repo-folder>

# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python src/main.py
```

## Future Improvements

- Experiment with LightGBM as an additional gradient boosting baseline.
- Add cross-validation for more robust performance estimates.
- Threshold tuning based on precision-recall tradeoff rather than default 0.5.
- Package preprocessing and feature engineering into a scikit-learn `Pipeline`/`ColumnTransformer` for cleaner deployment.
- Add unit tests for preprocessing and feature engineering functions.

## Author

Saim Ansari
Deputy Director, IEEE RAS Technical Team | BS Robotics and Intelligent Systems, Bahria University Islamabad
Portfolio: [saimansari.me](https://saimansari.me) | GitHub: [github.com/saim-ansari-tech](https://github.com/saim-ansari-tech)

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

# 🏠 Indian House Price Prediction

A machine learning regression project that predicts residential property prices using structured housing data from multiple Indian cities.

This project was built as part of my Machine Learning learning journey and focuses on building a clean, reproducible ML workflow rather than chasing the highest accuracy.

---

# Project Objectives

- Understand the complete ML workflow
- Perform Exploratory Data Analysis (EDA)
- Clean and preprocess real-world data
- Build a regression model
- Evaluate model performance
- Apply engineering improvements for better data quality and reproducibility

---

# Dataset

## Features

| Feature | Description |
|----------|-------------|
| bhk | Number of bedrooms |
| propertytype | Property type |
| location | City |
| sqft | Built-up area (square feet) |

### Target

```
totalprice
```

---

# Project Workflow

```
Raw Dataset
      │
      ▼
Exploratory Data Analysis
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
      │
      ▼
Pipeline
      │
      ▼
Linear Regression
      │
      ▼
Model Evaluation
```

---

# Repository Structure

```
indian-house-price-prediction/

├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_loading.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_model_training.ipynb
│   ├── 05_model_evaluation.ipynb
│   ├── 06_exploratory_data_analysis.ipynb
│   ├── 07_engineering_refactor.ipynb
│   ├── 08_duplicate_leakage_analysis.ipynb
│   └── 09_grouped_train_test_split.ipynb
│
├── models/
│
├── reports/
│
├── requirements.txt
└── README.md
```

---

# Data Preprocessing

The project includes:

- Missing value inspection
- Duplicate removal
- Invalid area filtering
- Categorical encoding using One-Hot Encoding
- Train/Test splitting
- Group-aware evaluation
- Scikit-learn Pipeline

---

# Model

Current baseline model:

- Linear Regression

---

# Evaluation Metrics

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² Score

---

# Engineering Improvements

Compared to the initial baseline, the project includes:

- Removal of physically invalid property sizes
- Removal of exact duplicate records
- Pipeline-based preprocessing and training
- Group-aware train/test split to reduce feature leakage

---

# Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Jupyter Notebook

---

# Learning Outcomes

Through this project I learned:

- End-to-end ML workflow
- Data cleaning
- Feature engineering
- Exploratory Data Analysis
- Regression modeling
- Pipeline creation
- Model evaluation
- Engineering practices for reproducible ML workflows

---

# Future Improvements

This project is intentionally frozen as **Version 1.0**.

Future versions will include techniques learned later in my ML roadmap, such as:

- Ridge Regression
- Decision Trees
- Random Forest
- Hyperparameter Tuning

---

## Author

**Bhushan Ahire**

MCA (Final Year)

Machine Learning & Backend Engineering
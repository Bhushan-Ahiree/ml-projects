# 🏠 Indian House Price Prediction

A machine learning regression project that predicts residential property prices using structured housing data from multiple Indian cities.

This project was built as part of my Machine Learning learning journey and focuses on building a **clean, reproducible, and interview-ready ML workflow** rather than chasing the highest possible accuracy.

---

# 🎯 Project Objectives

* Understand an end-to-end machine learning workflow
* Perform Exploratory Data Analysis (EDA)
* Clean and prepare real-world housing data
* Engineer relevant features
* Build regression models
* Evaluate models using appropriate metrics
* Identify and reduce train/test contamination caused by repeated feature groups
* Build a reproducible preprocessing and model pipeline
* Persist the trained model for later use

---

# 📊 Dataset

The raw dataset contains residential property information from multiple Indian cities.

## Features

| Feature        | Description                  |
| -------------- | ---------------------------- |
| `bhk`          | Number of bedrooms           |
| `propertytype` | Property type                |
| `location`     | City/locality                |
| `sqft`         | Built-up area in square feet |

## Target

```text
totalprice
```

The `pricepersqft` column was excluded from model training because it is directly related to the target price and can introduce target-entangled information into the model.

---

# 🔄 Project Workflow

```text
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
Refined Dataset
     │
     ▼
Group-Aware Train/Test Split
     │
     ▼
Preprocessing Pipeline
     │
     ▼
Model Training
     │
     ├───────────────┐
     ▼               ▼
Linear Regression  Tree-Based Models
     │               │
     └───────┬───────┘
             ▼
      Model Evaluation
             │
             ▼
       Model Comparison
             │
             ▼
    Persisted ML Pipeline
```

---

# 📁 Repository Structure

```text
indian-house-price-prediction/

├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_model_training.ipynb
│   ├── 05_model_evaluation.ipynb
│   ├── 06_model_comparison.ipynb
│   ├── 07_engineering_refactor.ipynb
│   ├── 08_duplicate_leakage_analysis.ipynb
│   └── 09_grouped_train_test_split.ipynb
│
├── models/
│   └── house_price_pipeline.pkl
│
├── reports/
│
├── requirements.txt
└── README.md
```

---

# 🧹 Data Preprocessing

The project includes:

* Missing-value inspection
* Duplicate analysis and removal
* Invalid property-size filtering
* Feature selection
* Categorical encoding using One-Hot Encoding
* Group-aware train/test splitting
* Scikit-learn Pipeline for preprocessing and model training

The refined dataset contains:

```text
13,297 rows
5 columns
```

The model uses the following four input features:

```text
bhk
propertytype
location
sqft
```

---

# 🔐 Group-Aware Evaluation

The dataset contains repeated combinations of the same input features:

```text
bhk + propertytype + location + sqft
```

These repeated feature groups can have different target prices.

A conventional random train/test split can therefore place rows from the same feature group in both training and test sets.

To

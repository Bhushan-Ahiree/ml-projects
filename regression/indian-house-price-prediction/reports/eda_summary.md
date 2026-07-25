# 📊 Exploratory Data Analysis (EDA) Summary

## Project

**Indian House Price Prediction**

---

## Objective

Understand the dataset, identify data quality issues, explore feature distributions, and gather insights before building Machine Learning models.

---

# Dataset Overview

| Property | Value |
|----------|------:|
| Total Records | 14,119 |
| Total Features | 6 |
| Numerical Features | 4 |
| Categorical Features | 2 |
| Missing Values | 0 |
| Duplicate Records | 92 |

---

# Features

| Column | Type | Description |
|---------|------|-------------|
| bhk | Numerical | Number of bedrooms |
| propertytype | Categorical | Type of property |
| location | Categorical | Property location |
| sqft | Numerical | Built-up area (sq ft) |
| pricepersqft | Numerical | Price per square foot |
| totalprice | Target | Total property price |

---

# Data Quality Assessment

## Missing Values

- No missing values found.

## Duplicate Records

- 92 duplicate rows detected.
- Duplicates will be removed during preprocessing.

## Data Types

- Numerical and categorical features are correctly identified.

---

# Exploratory Analysis

## Property Type

- Multiple property types are present.
- Distribution is imbalanced across categories.

---

## Location

- Properties are distributed across multiple locations.
- Some locations contain significantly more listings.

---

## BHK Distribution

- The majority of properties fall within common residential BHK categories.

---

## Area (sqft)

The `sqft` feature is highly right-skewed.

Several extremely large property sizes were identified, including:

- 799,284 sqft
- 302,260 sqft
- 200,000 sqft

These values significantly stretch the distribution and will require further investigation during preprocessing.

---

## Total Price

Property prices are not uniformly distributed.

Higher-priced properties form a long right tail, indicating potential high-value outliers.

---

## Relationship Between Area and Price

Scatter plot analysis indicates a positive relationship between property area and total price.

Larger properties generally tend to have higher prices.

---

# Potential Data Leakage

The dataset contains both:

- `pricepersqft`
- `totalprice`

Since:

```
Total Price ≈ Area × Price per Sqft
```

Using `pricepersqft` to predict `totalprice` may introduce data leakage.

The initial model will therefore use:

### Features (X)

- bhk
- propertytype
- location
- sqft

### Target (y)

- totalprice

`pricepersqft` will be excluded from the first model and evaluated separately later.

---

# Key Findings

- Dataset is clean with no missing values.
- Duplicate records are present.
- Area and price distributions are right-skewed.
- Several extreme outliers exist in the `sqft` feature.
- Both numerical and categorical preprocessing will be required.
- The dataset is suitable for a supervised regression problem.

---

# Next Steps

- Remove duplicate records.
- Handle categorical variables.
- Investigate outliers.
- Split features and target.
- Train baseline regression models.
- Compare model performance.

---

# Conclusion

The dataset is well-suited for a house price prediction project. Initial EDA identified duplicate records, highly skewed numerical features, and potential data leakage from the `pricepersqft` feature. These findings will guide the preprocessing and modeling stages to build a reliable regression model.
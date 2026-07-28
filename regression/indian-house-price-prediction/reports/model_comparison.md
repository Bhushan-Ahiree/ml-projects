# Model Performance

## Baseline (Cleaned Dataset)

Linear Regression

MAE : 6,693,226.64

RMSE : 18,087,033.08

R² : 0.2359

---

## After Engineering Refactor

Linear Regression

MAE : 5,799,284.17

RMSE : 17,091,286.74

R² : 0.3789

---

## Conclusion

Removing physically impossible area values, removing exact duplicate rows, and training through a Pipeline improved all evaluation metrics without changing the model.

This confirms that data quality had a measurable impact on model performance.
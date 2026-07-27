# Engineering Decisions

## Decision 001
Removed `pricepersqft`.

Reason:
Target leakage.

Trade-off:
Slight reduction in available information, but prevents unrealistic model performance.

---

## Decision 002
Kept extreme sqft values during the first training iteration.

Reason:
Wanted to establish a baseline before applying data-quality rules.

Future Work:
Review and document an outlier policy.


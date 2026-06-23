# Validation Benchmarks

These numbers are the ground truth for this project.
Every pipeline stage, every PostgreSQL load, and every dashboard
must reconcile against these figures within 0.1% tolerance.

If any output does not match, stop. Do not proceed.
Investigate the loading or transformation step before continuing.

---

## Source File

| Property | Value |
|---|---|
| Filename | online_retail_II.xlsx |
| Sheets | Year 2009-2010, Year 2010-2011 |
| MD5 fingerprint | [record here after first load] |

---

## Raw Data Benchmarks

| Metric | Value |
|---|---|
| Sheet 1 rows (2009-2010) | 525,461 |
| Sheet 2 rows (2010-2011) | 541,910 |
| Combined raw rows | 1,067,371 |
| Raw columns | 8 |
| Date range | 2009-12-01 to 2011-12-09 |
| Unique countries (raw) | 43 |
| Unique StockCodes (raw) | 5,305 |
| Unique Customer IDs (raw) | 5,942 |

---

## Cleaning Benchmarks

| Step | Rows Before | Rows After | Rows Removed |
|---|---|---|---|
| Exact duplicate removal | 1,067,371 | 1,033,036 | 34,335 |
| Separate returns (neg qty) | 1,033,036 | 1,010,086 | 22,950 |
| Separate adjustments (neg price) | 1,010,086 | 1,010,081 | 5 |
| Final sales rows | 1,010,081 | 1,007,914 | 2,167* |

*Additional rows removed during product/invoice validation

---

## Staging File Benchmarks

| File | Rows | Notes |
|---|---|---|
| sales_main.csv | 1,007,914 | Positive sales only |
| returns_cancellations.csv | 22,950 | Negative quantity rows |
| accounting_adjustments.csv | 5 | Negative price rows |
| non_merchandise_codes.csv | [count] | Reference list |

---

## Revenue Benchmarks

| Metric | Value |
|---|---|
| Total revenue (all codes) | £20,476,634.00 |
| Merchandise revenue only | £19,701,497.66 |
| Non-merchandise revenue | £775,136.34 |
| UK revenue | £17,410,570 |
| UK revenue share | 85.0% |
| Total orders (distinct invoices) | 40,078 |

---

## Warehouse Benchmarks (PostgreSQL)

After loading staging files into PostgreSQL, run validation queries.
All results must match within 0.1% tolerance.

```sql
-- Revenue check
SELECT ROUND(SUM(revenue)::numeric, 2) AS total_revenue
FROM fact_sales;
-- Expected: 20476634.00

-- Row count check
SELECT COUNT(*) AS row_count FROM fact_sales;
-- Expected: 1007914

-- Country check
SELECT COUNT(DISTINCT country_key) FROM fact_sales;
-- Expected: 43

-- Anomaly check
SELECT COUNT(*) FROM ml_anomaly_scores WHERE is_anomaly = TRUE;
-- Expected: 139

-- Forecast check
SELECT COUNT(*) FROM revenue_forecast;
-- Expected: 90
```

---

## Forecasting Benchmarks

| Metric | Value |
|---|---|
| Forecasting series rows (continuous) | 739 |
| Observed transaction days | 604 |
| Zero-fill days added | 135 |
| Training rows | 649 |
| Holdout rows | 90 |
| Training end date | 2011-09-10 |
| Holdout start date | 2011-09-11 |
| Merchandise revenue sum (series) | £19,701,497.66 |

---

## Model Performance Benchmarks

### Seasonal Naive Baseline (minimum bar)
| Metric | Value |
|---|---|
| MAE | 15,121.75 |
| RMSE | 24,567.28 |

### SARIMA (best candidate)
| Metric | Value |
|---|---|
| MAE | 22,662.61 |
| RMSE | 33,064.93 |
| Result | Did not beat baseline |

### XGBoost V1 (selected model)
| Metric | Value |
|---|---|
| MAE | 11,805.29 |
| RMSE | ~21,450 |
| MAE improvement vs baseline | −21.9% |
| RMSE improvement vs baseline | −12.6% |
| Max absolute error | 143,514.33 (Dec 9 spike) |
| Avg forecast revenue | £38,592.30 |
| Avg actual revenue | £43,947.01 |
| Forecast bias | Conservative (underpredicts by ~12%) |

---

## RFM Benchmarks

| Metric | Value |
|---|---|
| Customers segmented | 5,878 |
| Champion customers | 1,268 |
| Champion revenue | £11,795,212 |
| Champion revenue share | 67.89% |
| Lost customers | 1,348 |
| Lost revenue | £163,148 |

---

## Anomaly Benchmarks

| Metric | Value |
|---|---|
| Country-day rows scored | 2,639 |
| Rows skipped (low history) | 171 |
| Countries scored | 18 |
| Total anomalies | 139 |
| High anomalies (positive spikes) | 117 (84.17%) |
| Low anomalies (demand drops) | 22 (15.83%) |
| Contamination parameter used | 0.05 |
| Min observations threshold | 30 |

---

## V2 Model Benchmarks

All V2 metrics are ground truth for this project.
Evaluated on the same 90-day holdout window as V1.
Any pipeline output that does not match these numbers
indicates a calculation or data error.

### V2 Forecast Error Benchmarks
| Metric | V1 (baseline) | V2 (current) | Improvement |
|---|---|---|---|
| MAE | £12,258 | £7,248 | +40.87% |
| RMSE | £20,764 | £15,641 | +24.67% |
| Spike-Day MAE | £42,755 | £29,408 | +31.22% |
| R² | 34.89% | 63.06% | +80.72% |
| WAPE | 24.38% | 14.41% | +40.87% |
| Bias | −8.54% | −9.08% | −6.29% |

### V2 Holdout Benchmarks
| Metric | Value |
|---|---|
| Holdout start | 2011-09-11 |
| Holdout end | 2011-12-09 |
| Holdout days | 90 |
| Peak actual revenue | £200,919 |
| V2 forecast on peak day | £75,438 |
| Peak day error | £125,481 |
| Max V1 error (same day) | £139,473 |
| Minimum error day | £16 |

### V2 Customer Segmentation Benchmarks (Corrected)
These numbers are from the corrected V2 dashboard.
The earlier version had inverted segment labels — now fixed.

| Segment | Count | Avg Value | Avg Frequency | Avg Recency Days |
|---|---|---|---|---|
| At Risk | 1,411 | £475 | 1.69 | 292.6 |
| Loyal Customers | 1,341 | £2,298 | 5.58 | 100.0 |
| Champions | 1,317 | £9,552 | 17.71 | 25.1 |
| Potential Loyalists | 968 | £907 | 3.00 | 173.1 |
| Lost Customers | 841 | £198 | 1.04 | 515.0 |
| **Total** | **5,878** | — | — | — |

Validation check — Champions must satisfy all three conditions:
- Highest average monetary value ✓ (£9,552)
- Highest average frequency ✓ (17.71)
- Lowest average recency days ✓ (25.1)

If any Champions row violates any of these three conditions,
the RFM scoring has an error and must be recomputed.

### V2 Dashboard Count
| Version | Dashboards | Files |
|---|---|---|
| V1 | 4 | Revenue Overview, RFM, Forecast Performance, Anomaly |
| V2 | 5 | V1 vs V2 Comparison, Ops Monitoring, Business Impact, Customer Retention x2 |
| Total | 9 | — |
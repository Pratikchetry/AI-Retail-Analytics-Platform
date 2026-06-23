# Business Rules

These rules define how the data must be interpreted in all queries,
dashboards, and model outputs. Violating any of these rules produces
metrics that are either inflated, understated, or misleading.

---

## Rule 1 — Revenue Calculation
Revenue is always computed as Quantity multiplied by Price at the
invoice line level before aggregation.
Aggregated revenue fields in views and fact tables use this computation.
Never aggregate Price or Quantity independently and then multiply.

## Rule 2 — Merchandise Revenue Filter
Any product revenue metric, product ranking, or forecasting target
must filter to WHERE is_merchandise = TRUE unless explicitly stated otherwise.
Including postage, service charges, and manual adjustments in product
revenue overstates demand by approximately £775,136 over the full period.
Total revenue (all codes) is valid for overall business reporting.
Merchandise revenue is the correct target for demand forecasting.

## Rule 3 — Returns Are Not Revenue Deductions
Returns and cancellations are stored in fact_returns_cancellations.
They are not stored as negative rows in fact_sales.
Do not subtract returns from fact_sales revenue to get net revenue.
If net revenue (after returns) is needed, join fact_returns_cancellations
separately and compute the adjustment explicitly.

## Rule 4 — Customer ID Nulls Are Unknown, Not Zero
Transactions with no Customer ID are assigned customer_key = 0.
This represents Unknown Customer, not a specific customer.
Summing revenue by customer_key = 0 gives the total anonymous transaction
revenue but does not represent a real customer.
Always exclude customer_key = 0 from customer-level analysis such as
average spend per customer, RFM segments, and top customer rankings.

## Rule 5 — Currency Is GBP Only
All monetary values in this dataset are in British Pounds Sterling (£).
No currency conversion has been applied.
Any dashboard or report displaying values in other currencies (INR, USD, EUR)
is showing incorrect formatting. The underlying numbers are GBP.

## Rule 6 — Date Grain for Forecasting Is Daily
The forecasting series uses a continuous daily calendar from 2009-12-01
to 2011-12-09, including 135 zero-revenue days filled with zeros.
Zero-revenue days represent real calendar days with no recorded transactions.
They are not missing data. They must not be dropped from time-series models.

## Rule 7 — Non-Merchandise StockCodes
The following StockCodes are classified as non-merchandise in dim_product:
POST, DOT, M, BANK CHARGES, AMAZONFEE, S, DCGS0076
This list may be incomplete. Any StockCode with a description containing
postage, manual, bank, fee, sample, or adjust should be reviewed
and classified before inclusion in product-level metrics.

## Rule 8 — Anomaly Scores Apply Only to Scored Countries
18 of 43 countries have anomaly scores in ml_anomaly_scores.
25 countries had fewer than 30 observations and were excluded.
Any query joining fact_sales to ml_anomaly_scores will produce
null anomaly scores for unscored countries. This is expected behavior
and must be handled with a COALESCE or LEFT JOIN in dashboard queries.

## Rule 9 — Forecast Covers Only the 90-Day Holdout
revenue_forecast contains 90 rows covering 2011-09-11 to 2011-12-09.
It does not contain training period predictions.
It does not contain future predictions beyond 2011-12-09.
Joining revenue_forecast to fact_sales on dates before 2011-09-11
will return no forecast rows for those dates. This is correct behavior.

## Rule 10 — RFM Segments Exclude Anonymous Customers
ml_rfm_segments contains only customers with valid Customer ID values.
It does not include the Unknown Customer surrogate (customer_key = 0).
Total customers segmented: 5,878.
Total unique Customer IDs in raw data: 5,942.
The gap of 64 customers represents IDs present in raw data but filtered
during segmentation due to insufficient transaction history.
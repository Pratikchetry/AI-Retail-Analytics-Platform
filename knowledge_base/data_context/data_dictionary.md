# Data Dictionary

## Raw Source Columns (online_retail_II.xlsx)

### Invoice
Type: String
Description: Transaction identifier. Invoices starting with C indicate
cancellations or returns. All other invoices are positive sales transactions.
Known issues: None beyond the C-prefix pattern for returns.

### StockCode
Type: String
Description: Product or operational code identifier.
Some codes represent non-merchandise items such as postage, service charges,
and manual adjustments. These are flagged in dim_product.
Known issues: Codes like M, POST, DOT, BANK CHARGES, AMAZONFEE are not
physical merchandise and must be excluded from product revenue analysis.

### Description
Type: String
Description: Text description of the product or service code.
Missing in 4,382 rows. Missing descriptions are retained where the
StockCode is still valid for revenue attribution.

### Quantity
Type: Integer
Description: Units sold or returned per invoice line.
Negative Quantity values indicate returns or cancellations.
22,950 rows have negative Quantity and are stored in fact_returns_cancellations.

### InvoiceDate
Type: Datetime
Description: Timestamp of the transaction. Used as the primary time dimension.
Aggregated to daily grain for time-series analysis and forecasting.

### Price
Type: Float (GBP)
Description: Unit price per item in British Pounds Sterling.
Revenue is computed as Quantity multiplied by Price.
Negative Price rows (5 total) represent accounting adjustments and are
stored in fact_accounting_adjustments.
Currency: GBP only. Any display showing INR or other currency is incorrect.

### Customer ID
Type: Float (effectively integer, stored with decimal)
Description: Unique customer identifier. Missing in 243,007 rows.
Missing Customer ID rows are assigned surrogate key 0 (Unknown Customer)
in the warehouse. They are excluded from RFM and customer-level analysis.

### Country
Type: String
Description: Country of the customer or transaction.
43 unique countries present. United Kingdom dominates with 85% of revenue.

---

## Warehouse Tables

### fact_sales
Grain: one row per invoice line item (positive sales only)
Key columns: order_date, revenue (quantity * price), quantity, invoice,
product_key, customer_key, country_key
Excludes: returns, adjustments, non-validated rows

### fact_returns_cancellations
Grain: one row per return or cancellation line
Source: negative Quantity rows from raw data
Note: not mixed into fact_sales to prevent revenue understatement

### fact_accounting_adjustments
Grain: one row per accounting adjustment entry
Source: negative Price rows from raw data (5 rows total)

### dim_product
Key columns: product_key, stock_code, description, is_merchandise, product_type
is_merchandise: TRUE for physical products, FALSE for postage/service/manual
product_type values: merchandise, postage, service, adjustment, manual, unknown

### dim_customer
Key columns: customer_key, customer_id
customer_key = 0 is the Unknown Customer surrogate for null Customer ID rows

### dim_country
Key columns: country_key, country_name

### dim_date
Key columns: date_key, full_date, year, month, day_of_week, is_weekend,
week_of_year, quarter, is_month_end

### ml_anomaly_scores
Grain: one row per scored country-day observation
Key columns: order_date, country_name, daily_revenue, daily_orders,
anomaly_score, is_anomaly, anomaly_direction
anomaly_direction values: high, low, normal
Only scored rows are present. Skipped countries are not in this table.

### revenue_forecast
Grain: one row per holdout day (90 rows total)
Key columns: order_date, actual_revenue, forecast_revenue, abs_error, model_name
Covers: 2011-09-11 to 2011-12-09
Model: xgboost (V1)

### ml_rfm_segments
Grain: one row per customer with valid Customer ID
Key columns: customer_id, rfm_segment, recency_score, frequency_score,
monetary_score, rfm_score

### feature_daily_enriched (planned for V2)
Grain: one row per calendar day
Key columns: order_date, is_uk_public_holiday, days_to_next_holiday,
is_peak_season, daily_active_customers, avg_basket_value, large_order_flag
Status: not yet created

---

## Computed Fields

### revenue
Computed as: Quantity multiplied by Price
Applied in: fact_sales, all views
Always positive in fact_sales (returns are excluded)

### is_merchandise
Source: dim_product
Logic: FALSE for StockCodes identified as non-physical items
Used in: all revenue metrics, forecasting target selection, product rankings

### merchandise_revenue
Computed as: SUM of revenue WHERE is_merchandise is TRUE
Used in: forecasting (primary target), filtered dashboard metrics

### anomaly_direction
Computed as: HIGH if is_anomaly is TRUE and revenue exceeds country median,
LOW if is_anomaly is TRUE and revenue is below country median, else NORMAL
Stored in: ml_anomaly_scores
# Tableau Dashboards — Retail Revenue Intelligence

This folder contains all Tableau dashboard assets for the
Retail Revenue Intelligence & Anomaly Detection project.

---

## Dashboard Overview

| Dashboard | File | Description |
|---|---|---|
| Revenue Overview | Revenue_overview_dashboard.png | Total revenue, daily trend, country breakdown |
| RFM Customer Segmentation | RFM_Customer_segmentation_dash.png | Customer segments, revenue contribution, top customers |
| Forecast Performance | Forecast_performance_dashboard.png | XGBoost V1 vs actual, error timeline, KPIs |
| Anomaly Monitoring | Anomaly_monitoring_dashboard.png | Anomaly count by country, timeline, high vs low split |

---

## Data Source

All dashboards connect directly to the **PostgreSQL retail_db warehouse**.
No dashboard reads from flat CSV files.

Connection: PostgreSQL localhost, database retail_db

Tables used:
- `fact_sales` — revenue and orders
- `dim_product` — product classification including is_merchandise flag
- `dim_customer` — customer keys
- `dim_country` — country names
- `dim_date` — date dimensions
- `ml_rfm_segments` — RFM segment assignments
- `ml_anomaly_scores` — scored anomaly flags with direction
- `revenue_forecast` — XGBoost V1 holdout predictions

---

## Dashboard 1 — Revenue Overview

**File:** `Revenue_overview_dashboard.png`

### What It Shows
- Total revenue, total orders, and countries covered (KPI cards)
- Daily revenue trend chart across the full 2009–2011 period
- Revenue by country (top 10 bar chart)
- Orders by country (top 10 bar chart)
- Date range filter (slider)
- Business narrative insight panel

### Key Metrics Displayed
| Metric | Value |
|---|---|
| Total Revenue | £20,476,634 |
| Total Orders | 40,078 |
| Countries Covered | 43 |
| UK Revenue | £17,410,570 (85%) |
| Peak Daily Revenue | £200,919 |

### Business Insight
The United Kingdom is the dominant market by both revenue and order
volume, contributing far more than any other country. EIRE, Netherlands,
Germany, and France form the next tier but the business remains
strongly UK-centred. Revenue performance and anomaly patterns are
driven primarily by UK market dynamics.

### Filters Available
- Order Date (range slider)

---

## Dashboard 2 — RFM Customer Segmentation

**File:** `RFM_Customer_segmentation_dash.png`

### What It Shows
- Total customers, champion count, total revenue, champion revenue % (KPIs)
- Segment revenue contribution (bar chart)
- Customer segment distribution by count (bar chart)
- Average RFM metrics by segment (cross-tab heatmap)
- Top customers by revenue (table)
- Segment filter (multi-select)

### Key Metrics Displayed
| Metric | Value |
|---|---|
| Total Customers | 5,878 |
| Champion Customers | 1,268 |
| Champion Revenue Share | 67.89% |
| Avg Champion Spend | £9,302 |
| Avg Lost Customer Spend | £343 |
| Avg Champion Days Since Purchase | 19 |
| Avg Lost Customer Days Since Purchase | 568 |

### Segment Summary
| Segment | Customers | Revenue | Avg Spend |
|---|---|---|---|
| Champions | 1,268 | £11,795,212 | £9,302 |
| Loyal Customers | 1,423 | £2,709,526 | £1,904 |
| At Risk — High Value | 453 | £1,428,405 | £3,625 |
| At Risk — Frequent | 516 | — | £615 |
| Potential Loyalists | 394 | — | £408 |
| New Customers | 476 | — | £908 |
| Lost | 1,348 | £163,148 | £343 |

### Business Insight
Losing one Champion customer has the same revenue impact as losing
approximately 27 Lost-segment customers. At Risk — High Value customers
(453 customers, £3,625 average spend, not seen in 366 days) represent
the highest-priority reactivation target.

### Filters Available
- Segment (multi-select checkbox)

### Known Issue
The dashboard currently displays revenue in ₹ (INR) due to a Tableau
locale formatting setting. All values are GBP (£). This will be corrected
in the next workbook version.

---

## Dashboard 3 — Forecast Performance

**File:** `Forecast_performance_dashboard.png`

### What It Shows
- Avg forecast revenue, avg actual revenue, avg error, max error (KPIs)
- Actual vs forecast overlay chart (90-day holdout)
- Forecast error over time chart (absolute error by day)
- Date range filter (slider)
- Model summary narrative panel

### Key Metrics Displayed
| Metric | Value |
|---|---|
| Holdout Period | 2011-09-11 to 2011-12-09 (90 days) |
| Avg Actual Revenue | £43,947.01 |
| Avg Forecast Revenue | £38,592.30 |
| Avg Absolute Error (MAE) | £11,805.29 |
| Max Absolute Error | £143,514.33 |
| RMSE Improvement vs Baseline | −12.6% |
| MAE Improvement vs Baseline | −21.9% |

### Model Used
XGBoost V1 — trained on merchandise revenue with 17 engineered features
including lag variables, rolling averages, calendar features, and
elapsed-time signal. Top feature: orders_rolling_mean_7 (SHAP 7,273).

### How To Read This Dashboard
- **Actual vs Forecast chart:** Blue/orange lines show where the model
  tracks reality and where it diverges. The weekly rhythm is captured
  well. Large gaps indicate spike days.
- **Error chart:** Shows absolute error per day. Most days show low error.
  The December 9 spike (£143,514 error) is clearly visible as the
  outlier at the far right.

### Business Interpretation
XGBoost captures the weekly revenue cycle well and performs strongly
on normal and mid-range trading days. The model is slightly conservative
(underpredicts by ~12% on average) and its largest errors occur on
rare extreme spike days. This makes it useful for operational planning
but not sufficient alone for predicting one-off demand shocks.

### Filters Available
- Date range (slider, covers holdout period only)

---

## Dashboard 4 — Anomaly Monitoring

**File:** `Anomaly_monitoring_dashboard.png`

### What It Shows
- Countries with anomalies, total anomalies, high anomaly share (KPIs)
- Anomaly count by country (bar chart)
- Anomaly timeline — all country-day observations with anomalies highlighted
- High vs low anomaly split (bar chart)
- Country filter (multi-select checkbox)
- Business narrative panel

### Key Metrics Displayed
| Metric | Value |
|---|---|
| Countries with Anomalies | 18 |
| Total Anomalies | 139 |
| High Anomaly Share | 84.17% (117 anomalies) |
| Low Anomaly Share | 15.83% (22 anomalies) |
| UK Anomaly Count | 31 |
| Germany Anomaly Count | 20 |

### How To Read This Dashboard
- **Anomaly count chart:** Bars show how many anomaly days each country had.
  Higher bars do not mean worse performance — UK has the most anomalies
  because it has the most trading activity.
- **Timeline:** Orange dots are anomalous country-day observations. The
  single dot at £200K at the far right is the December 9 2011 UK spike.
  The concentration of orange in the upper range confirms most anomalies
  are positive demand spikes, not collapses.
- **High vs Low split:** 117 high (positive spike) vs 22 low (demand drop).
  This tells the business that unusual behavior is mostly an opportunity
  signal, not a warning signal.

### Business Interpretation
139 unusual country-day observations were detected across 18 countries.
84% are classified as high anomalies (positive demand spikes above country
median), meaning the system is primarily detecting unexpected positive
demand events rather than operational problems. UK has the highest count
but Germany, France, and EIRE also show repeated unusual behavior.

### Filters Available
- Country Name (multi-select checkbox, all 18 scored countries)

---

## How Dashboards Are Connected to the Warehouse

```
PostgreSQL retail_db
        │
        ├── fact_sales (joined to dim_product for is_merchandise filter)
        ├── ml_rfm_segments
        ├── ml_anomaly_scores
        └── revenue_forecast
        │
        ▼
Tableau Desktop (live connection)
        │
        ├── Revenue Overview Dashboard
        ├── RFM Customer Segmentation Dashboard
        ├── Forecast Performance Dashboard
        └── Anomaly Monitoring Dashboard
```

All views are built on top of validated warehouse data.
Revenue totals reconcile to £20,476,634 as per validation_benchmark.md.

---

## What To Add Next

The following improvements are planned before V2 dashboard release:

- [ ] Fix currency display from ₹ to £ in RFM dashboard
- [ ] Add SHAP feature importance chart to Forecast dashboard
- [ ] Add V1 vs V2 model comparison panel to Forecast dashboard
- [ ] Add spike-day vs normal-day error breakdown chart
- [ ] Publish workbooks to Tableau Public with public link
- [ ] Add product-level dashboard (ABC analysis, top products)
- [ ] Add customer retention trend dashboard (RFM movement over time)
- [ ] Connect to BigQuery after GCP migration

---

## Notes for Reviewers

1. All revenue values are in GBP (£). INR display is a formatting bug.
2. The forecast dashboard covers only the 90-day holdout period (Sep–Dec 2011).
   It does not show training period predictions.
3. The anomaly dashboard covers only the 18 countries with sufficient
   history for IsolationForest scoring. 25 countries are not shown
   because they had fewer than 30 country-day observations.
4. RFM segments are a static snapshot computed at the time of notebook
   execution. They do not update automatically.# Tableau

## Files
- `retail_dashboard.twbx` — Main Tableau workbook (add this once built in Tableau Desktop/Public)
- `screenshots/` — PNG screenshots of each dashboard page for portfolio sharing

## Connection Setup
Data source: PostgreSQL (Live connection recommended over extract for real-time anomaly updates)

Host: localhost
Port: 5432
Database: retail_db
Username: (from .env)

## Dashboard Pages
1. Executive Summary — KPI scorecards
2. Revenue Trends — YoY chart + 90-day forecast overlay
3. Anomaly Alerts — ML flagged days
4. Customer RFM — Segment scatter plot with drill-through

---

## V2 Dashboards

Four new dashboards were built for the V2 phase.
All connect directly to the validated PostgreSQL warehouse.
All metrics are in GBP (£). Holdout period: 2011-09-11 to 2011-12-09.

---

### Dashboard 5 — V1 vs V2 Forecast Performance

**File:** `workbooks/V1_vs_V2_Forecast_Performance_Dashboard.twb`
**Screenshot:** `screenshots/v2/V1_vs_V2_Forecast_Performance.png`

#### What It Shows
- Four KPI header cards: Best Improvement, Highest Accuracy,
  Largest Regression, Overall Assessment
- V1 vs V2 Statistical Performance Metrics grouped bar chart
  covering R², WAPE, and Bias side by side per model
- V1 vs V2 Forecast Error Metrics grouped bar chart
  covering MAE, RMSE, and Spike-Day MAE side by side
- Model filter (All / V1 / V2)

#### Key Numbers

**KPI Strip**
| KPI | Value |
|---|---|
| Best Improvement | MAE +40.87% |
| Highest Accuracy | R² = 0.63 |
| Largest Regression | Bias −6.29% |
| Overall Assessment | V2 Outperforms V1 |

**Statistical Metrics**
| Metric | V1 | V2 | Direction |
|---|---|---|---|
| R² | 34.89% | 63.06% | Higher is better — V2 wins |
| WAPE | 24.38% | 14.41% | Lower is better — V2 wins |
| Bias | −8.54% | −9.08% | V1 marginally less biased |

**Error Metrics**
| Metric | V1 | V2 | Improvement |
|---|---|---|---|
| MAE | £12,258 | £7,248 | +40.87% |
| RMSE | £20,764 | £15,641 | +24.67% |
| Spike-Day MAE | £42,755 | £29,408 | +31.22% |

#### Business Insight
V2 outperforms V1 on every primary error metric. The MAE improvement
of 40.87% means average daily forecast error dropped from £12,258 to
£7,248 — a £5,010 daily reduction. R² improved from 34.89% to 63.06%,
meaning V2 explains nearly double the revenue variance that V1 did.
WAPE dropped from 24.38% to 14.41%, confirming V2 is proportionally
more accurate relative to actual revenue levels.

The only regression is Bias at −9.08% versus V1 at −8.54%.
Both models underpredict on average. The 0.54 percentage point
difference is not operationally significant and does not offset
the 40.87% MAE improvement. The overall assessment is clear:
V2 should replace V1 as the primary operational forecasting model.

---

### Dashboard 6 — Forecast Monitoring & Operations Intelligence

**File:** `workbooks/Forecast_Monitoring_Operations_Intelligence_v2.twb`
**Screenshot:** `screenshots/v2/Forecast_Monitoring_Operations_Intelligence.png`

#### What It Shows
- Four KPI cards: RMSE, MAE, WAPE, R² Score
- Actual vs Predicted Revenue Trend overlay (Aug–Dec 2011)
- V1 Highest Forecast Error Days (top 10 worst days)
- V2 Highest Forecast Error Days (top 10 worst days)
- Forecast Error Monitoring timeline (absolute error over holdout)
- Revenue Distribution Analysis histogram (days per revenue band)
- Date range filter slider

#### Key Numbers

**V2 Model KPIs**
| Metric | Value |
|---|---|
| RMSE | £15,641 |
| MAE | £7,248 |
| WAPE | 14.4% |
| R² Score | 0.631 |
| Peak actual revenue (holdout) | £200,919 (Dec 9 2011) |
| V2 forecast on peak day | £75,438 |
| Peak day absolute error | £125,481 |

**V1 Top Forecast Error Days**
| Rank | Error Amount |
|---|---|
| 1 | £139,473 |
| 2 | £52,897 |
| 3 | £40,163 |
| 4 | £30,617 |
| 5 | £29,100 |
| 6 | £28,871 |
| 7 | £28,719 |
| 8 | £26,381 |
| 9 | £26,338 |
| 10 | £25,540 |

**V2 Top Forecast Error Days**
| Rank | Error Amount |
|---|---|
| 1 | £125,481 |
| 2 | £28,708 |
| 3 | £20,864 |
| 4 | £18,269 |
| 5 | £17,956 |
| 6 | £17,168 |
| 7 | £16,686 |
| 8 | £15,231 |
| 9 | £15,115 |
| 10 | £14,643 |

**Revenue Distribution (90-day holdout)**
| Revenue Band | Days |
|---|---|
| £0 — £25,000 | 6 |
| £25,000 — £50,000 | 18 |
| £50,000 — £75,000 | 22 |
| £75,000 — £100,000 | 19 |
| £100,000 — £125,000 | 10 |
| £125,000 — £150,000 | 5 |
| £150,000 — £175,000 | 2 |
| £175,000 — £200,000 | 1 |
| Above £200,000 | 1 |
| Minimum error day | £16 |

#### Business Insight
This dashboard serves as an operational monitoring panel showing
exactly when and where each model fails.

The actual vs predicted trend confirms V2 tracks the weekly cycle
closely from September through November. The December 9 spike at
£200,919 (V2 forecast: £75,438) is the single dominant error event
and is clearly identifiable across all three error charts.

Comparing V1 and V2 error rankings directly shows V2's structural
improvement beyond the average metric. V2's worst error is £125,481
versus V1's £139,473 — £13,992 better on the hardest single day.
More importantly, V2's second-worst error is £28,708 compared to V1's
£52,897 — a 45.6% reduction on the runner-up error day. This pattern
continues down the ranking, confirming V2 is more robust across the
entire error distribution, not just at the mean.

The Revenue Distribution histogram shows 65 of 90 holdout days
(72%) fell below £75,000. V2 performs strongly on this majority.
The 7 days above £125,000 drive a disproportionate share of total
forecast error — the known structural limitation of lag-based models
on a spiky retail revenue series with extreme outlier events.

---

### Dashboard 7 — V2 Forecasting System — Business Impact Analysis

**File:** `workbooks/V2_Forecasting_System_Business_Impact_Analysis.twb`
**Screenshot:** `screenshots/v2/V2_Business_Impact_Analysis.png`

#### What It Shows
- Business KPI strip: Best Improvement KPI, Spike KPI,
  Risk Reduction KPI, Executive Recommendation
- Forecast Performance Improvement bar chart (6 metrics,
  green = improved, orange = regression)
- Revenue Forecasting Risk Reduction grouped bar chart
  (MAE and RMSE V1 vs V2 absolute values)
- High-Revenue Day Forecast Accuracy (Spike-Day MAE V1 vs V2)
- Performance Category filter (Improved / Regression)
- Model filter (All / V1 / V2)

#### Key Numbers

**Business KPI Strip**
| KPI | Statement |
|---|---|
| Best Improvement | MAE reduced by 40.9% |
| Spike KPI | Spike-day forecast error reduced by 31.2% |
| Risk Reduction | Operational forecast risk significantly reduced |
| Executive Recommendation | Deploy V2 for operational planning and revenue forecasting |

**Performance Improvement by Metric**
| Metric | Improvement | Category |
|---|---|---|
| R² | +80.72% | Improved |
| MAE | +40.87% | Improved |
| WAPE | +40.87% | Improved |
| Spike-Day MAE | +31.22% | Improved |
| RMSE | +24.67% | Improved |
| Bias | −6.29% | Regression |

**Revenue Forecasting Risk Reduction**
| Metric | V1 | V2 | Reduction |
|---|---|---|---|
| MAE | £12,258 | £7,248 | £5,010/day |
| RMSE | £20,764 | £15,641 | £5,123 |

**High-Revenue Day Accuracy**
| Model | Spike-Day MAE |
|---|---|
| V1 | £42,755 |
| V2 | £29,408 |
| Improvement | £13,347 per spike day |

#### Business Insight
This dashboard translates model performance improvement into
financial and operational terms.

The £5,010 daily MAE improvement means that over a standard
90-day planning quarter, V2 produces forecasts that are
cumulatively £450,900 closer to actual revenue than V1.
For inventory, staffing, and cash flow planning, this represents
£450,900 less exposure to over or under-provisioning per quarter.

The spike-day MAE reduction of £13,347 per high-revenue day
directly addresses the most operationally damaging forecast
failures. High-revenue days are when inventory and logistics
decisions carry the highest cost of error. V2 reduces error
on these critical days by 31.2%.

5 of 6 metrics show improvement. The single regression (Bias
at −6.29%) is marginal — both V1 and V2 underpredict, and the
difference is 0.54 percentage points, which is not operationally
significant. The executive recommendation on the dashboard is
supported by the data: deploy V2 as the primary forecasting model.

---

### Dashboard 8 — Customer Segmentation & Retention Intelligence

**Files:**
- `workbooks/Customer_Segmentation_Retention_Intelligence.twb`

**Screenshots:**
- `screenshots/v2/Customer_Segmentation_Retention_Intelligence_1.png`
- `screenshots/v2/Customer_Segmentation_Retention_Intelligence_2.png`

---

#### Page 1 — Segment Distribution, Monetary Value, Action Matrix

**What It Shows**
- Customer Segment Distribution bar chart (count per segment)
- Average Monetary Value by Customer Segment bar chart
- Customer Retention Action Matrix (recommended action per segment)
- Customer Segment filter (multi-select)

**Segment Distribution**
| Segment | Customer Count |
|---|---|
| At Risk | 1,411 |
| Loyal Customers | 1,341 |
| Champions | 1,317 |
| Potential Loyalists | 968 |
| Lost Customers | 841 |
| **Total** | **5,878** |

**Average Monetary Value by Segment**
| Segment | Avg Monetary Value |
|---|---|
| Champions | £9,552 (highest) |
| Loyal Customers | £2,298 |
| Potential Loyalists | £907 |
| At Risk | £475 |
| Lost Customers | £198 (lowest) |

**Customer Retention Action Matrix**
| Segment | Recommended Action | Label |
|---|---|---|
| At Risk | Immediate Re-engagement | Priority (red) |
| Loyal Customers | Loyalty Programs | Core play (green) |
| Champions | Reward & Retain | VIP (blue) |
| Potential Loyalists | Upsell & Nurture | Grow (purple) |
| Lost Customers | Win-back Campaign | Re-activate (black) |

#### Page 1 Business Insight
Champions generate the highest average customer value at £9,552,
significantly outperforming all other segments. Retaining and
rewarding these customers is the top priority as they contribute
the greatest value per customer.

At Risk is the largest segment with 1,411 customers. With an
average monetary value of only £475, these customers are moderate
individual contributors — but the sheer volume makes this the
highest collective churn risk. Immediate re-engagement campaigns
targeting this group would protect the most customers simultaneously.

Lost Customers show the lowest average value at £198, confirming
they were likely low-value buyers who made a single small purchase.
Win-back campaigns for this group should use low-cost automated
approaches rather than high-touch outreach.

---

#### Page 2 — Purchase Frequency, Recency Risk, Action Matrix

**What It Shows**
- Average Purchase Frequency by Customer Segment bar chart
- Average Recency by Customer Segment bar chart
  (avg days since last purchase — higher = more inactive)
- Customer Retention Action Matrix (same as Page 1)
- Customer Segment filter

**Average Purchase Frequency**
| Segment | Avg Purchases |
|---|---|
| Champions | 17.71 (highest) |
| Loyal Customers | 5.58 |
| Potential Loyalists | 3.00 |
| At Risk | 1.69 |
| Lost Customers | 1.04 (lowest) |

**Average Recency (Days Since Last Purchase)**
| Segment | Avg Days Inactive | Risk Level |
|---|---|---|
| Lost Customers | 515.0 | Critical — permanent churn risk |
| At Risk | 292.6 | High — urgent reactivation needed |
| Potential Loyalists | 173.1 | Medium — monitor closely |
| Loyal Customers | 100.0 | Low — stable engagement |
| Champions | 25.1 | Lowest — active and recent |

#### Page 2 Business Insight
Champions purchase an average of 17.71 times — more than any
other segment — making them the most engaged customer group.
Their strong repeat purchasing behaviour highlights their
importance for long-term revenue and customer lifetime value.
Champions also have the lowest recency at 25.1 days, confirming
they are actively trading.

Lost Customers have been inactive for an average of 515 days —
over 17 months. The dashboard narrative notes that recovering
even a small portion of this segment through targeted win-back
campaigns could create additional revenue opportunity.
However, at 1.04 average purchases and £198 average value,
the expected return per recovered customer is low, so
campaigns should be low-cost and automated.

At Risk customers (292.6 days inactive, 1,411 count) represent
the most urgent operational concern. They have purchased 1.69
times on average and spent £475 — moderate individual value
but the largest segment by count. The window for successful
reactivation narrows significantly beyond 300 days of inactivity.

Potential Loyalists (173.1 days, 3.00 purchases, £907 value)
are the development opportunity. They have purchased multiple
times and have meaningful value but are drifting toward
inactivity. Upsell and nurture campaigns targeting this segment
can convert them toward the Loyal Customer tier before they
cross into At Risk territory.

### Dashboard 9 — Product Intelligence & Investment Strategy
- `File: workbooks/Product_Intelligence_Investment_Strategy.twb`
Screenshots:

-`screenshots/v2/Product_Intelligence_Investment_Strategy-1.png`
-`screenshots/v2/Product_Intelligence_Investment_Strategy-2.png`

#### Page 1 — What It Shows

Top Revenue Generating Products bar chart (top 10)
Top Selling Products by Quantity bar chart (top 10)
Product Investment Strategy distribution bar chart

#### Page 1 Key Numbers
##### Top 5 by Revenue:
ProductRevenueREGENCY CAKESTAND 3 TIER£330,590CREAM HANGING HEART T-LIGHT HOLDER£257,725JUMBO BAG RED RETROSPOT£182,681PAPER CRAFT, LITTLE BIRDIE£168,470PARTY BUNTING£148,318
##### Top 5 by Quantity:
ProductQuantityWORLD WAR 2 GLIDERS ASSTD DESIGNS106,139JUMBO BAG RED RETROSPOT96,757PACK OF 72 RETRO SPOT CAKE CASES94,884CREAM HANGING HEART T-LIGHT HOLDER94,203POPCORN HOLDER88,499
Investment Strategy: Monitor 3,172 · Invest More 810 ·
Premium Focus 371 · Marketing Opportunity 371
#### Page 2 — What It Shows

Revenue Contribution by Product % bar chart
Product Performance Matrix scatter plot (Revenue vs Quantity,
4 quadrants with reference lines at £100K and 50K units)

#### Page 2 Key Numbers

REGENCY CAKESTAND 3 TIER: 1.68% revenue contribution (highest)
CREAM HANGING HEART: 1.31%
Top 10 products combined: ~8.35% of total revenue
Quadrant distribution: Superstar (4 products) · Premium (3) ·
Mass Market (3) · Underperforming (majority)

#### Business Insight — Page 1
Revenue and volume leaders are different products. The highest-revenue
product (Cakestand, £330,590) has moderate volume. The highest-volume
product (WW2 Gliders, 106,139 units) has only £24,446 revenue.
Business decisions using only one dimension miss the full picture.
#### Business Insight — Page 2
Cream Hanging Heart T-Light Holder is the only true Superstar
(high revenue + high quantity). REGENCY CAKESTAND is a Premium
product (high revenue, lower quantity — premium pricing behavior).
Paper Craft Little Birdie's £168,470 from 1 order is a single
bulk purchase anomaly and should not be treated as demand signal.


### Dashboard 10 — Revenue Intelligence & Growth Analytics
-`File: workbooks/Revenue_Intelligence_Growth_Analytics.twb`
Screenshot: `screenshots/v2/Revenue_Intelligence_Growth_Analytics.png`
#### What It Shows

#### Five KPI cards: Total Revenue, Avg Monthly Revenue, Best Month,
Worst Month, YoY Growth
Monthly Revenue Trend line chart (Dec 2009 – Dec 2011)
Revenue Seasonality & YoY Comparison cross-tab (year × month)
Month-over-Month Revenue Growth % bar chart
Year-over-Year Revenue Performance bar chart

#### Key Numbers
KPIValueTotal Revenue£20,476,634Average Monthly Revenue£819,065Best MonthNov 2011 — £1,503,867Worst MonthFeb 2011 — £522,546YoY Growth−0.13%
#### Notable MoM Movements

Mar 2010: +50.56% (post-winter recovery)
Sep 2010: +32.57% (pre-holiday ramp)
Apr 2011: −24.25% (weakest 2011 period)
Sep 2011: +39.40% (strong H2 acceleration)
Dec 2011: −57.59% (partial month, not a real drop)

#### Business Insight
The −0.13% YoY figure masks the real story. H2 2011 outperformed
H2 2010 in September (+14.62%), with stability in October and
November. The negative YoY is driven by partial December 2011
data and a weak H1 2011. The business shows recovery momentum
through the second half of 2011.



## Notes for Reviewers

1. All currency values are GBP (£).
2. All forecast metrics evaluated on 2011-09-11 to 2011-12-09 holdout only.
   No training data was used in evaluation — the split was defined before
   any V2 model training began.
3. The RFM segment data was corrected between the first and second version
   of the customer dashboard. The corrected version correctly shows Champions
   with the highest monetary value (£9,552), highest frequency (17.71),
   and lowest recency days (25.1). This is consistent with standard RFM
   behavioral theory.
4. The Bias metric shows a slight regression in V2 (−9.08% vs −8.54%).
   Both models underpredict. The difference is 0.54 percentage points
   and is not operationally significant.
5. The December 9 2011 spike (£200,919 actual, £75,438 V2 forecast)
   remains the dominant error event in the holdout period and is
   visible across all forecast error charts.
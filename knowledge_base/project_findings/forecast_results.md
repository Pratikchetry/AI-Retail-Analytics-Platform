# Forecasting Results — V1

## Forecasting Target
Primary target: merchandise_revenue (daily)
Total revenue was available but excluded as primary target because
postage and service charges add operational noise not related to demand.
The gap between total and merchandise revenue is approximately £775,136
over the full two-year period.

## Time Series Properties
Full series: 739 continuous daily rows from 2009-12-01 to 2011-12-09
Observed transaction days: 604
Zero-revenue days added by calendar completion: 135
Calendar is confirmed continuous with no gaps.
ADF stationarity test: p-value 0.014, series is stationary in levels.
STL decomposition showed real trend, strong weekly seasonality, and
substantial residual variation with standard deviation of 10,051.

## Train-Test Split
Training window: 2009-12-01 to 2011-09-10 (649 rows)
Holdout window: 2011-09-11 to 2011-12-09 (90 rows)
The holdout period covers the late-year seasonal peak, making it the
most demanding evaluation window in the full series.

## Model Comparison Results

### Seasonal Naive Baseline
Method: forecast today as the value from the same day seven days ago.
MAE: 15,121.75
RMSE: 24,567.28
This is the minimum bar. Every model must beat this to justify complexity.

### SARIMA (best candidate tested)
Orders tested: (1,0,1)(1,0,1,7), (1,0,0)(1,0,1,7), (0,0,1)(1,0,1,7),
(1,0,1)(1,0,0,7), (1,0,1)(0,0,1,7), (2,0,1)(1,0,1,7), (1,0,2)(1,0,1,7)
Best SARIMA MAE: 22,662.61
Best SARIMA RMSE: 33,064.93
Result: SARIMA did not beat the seasonal naive baseline on this holdout window.
SARIMA was evaluated using a fixed 90-step-ahead projection from a single
fitted model. Walk-forward validation would be more realistic but was not
used due to computational cost at this stage. The volatile peak-season
holdout period likely penalized the fixed-fit projection approach.

### Random Forest
Results: [add after training]

### XGBoost V1 — Selected Model
MAE: 11,805.29
RMSE: approximately 21,450
MAE improvement vs naive baseline: minus 21.9%
RMSE improvement vs naive baseline: minus 12.6%
Average forecast revenue: £38,592.30
Average actual revenue: £43,947.01
Max absolute error: £143,514.33 (December 9 2011)
The model is slightly conservative overall, underpredicting by approximately 12%.

### LightGBM
Results: [add after training]

## Feature Importance (SHAP)
17 features were used. Top features by mean absolute SHAP value:

1. orders_rolling_mean_7: 7,273 — 7-day rolling average of order count
2. day_of_week: 6,379 — which day of the week it is
3. rolling_mean_7: 3,912 — 7-day rolling average of revenue
4. rolling_std_14: 3,620 — 14-day revenue volatility
5. days_since_start: 2,706 — elapsed time capturing baseline shift
6. orders_lag_1: 2,705 — yesterday's order count
7. lag_7: 2,290 — revenue from same weekday last week
8. orders_lag_7: 1,889 — order count from same weekday last week
9. lag_28: 1,682 — revenue from four weeks ago
10. rolling_mean_14: 1,432 — 14-day rolling revenue average
11-17 (remaining features below 1,100 mean SHAP)

## Key SHAP Interpretations
Order momentum beats revenue lags. orders_rolling_mean_7 is the top feature.
This means order activity is a leading indicator — the volume of recent orders
predicts revenue better than the revenue itself. Order count captures demand
breadth while revenue is more sensitive to individual large transactions.

day_of_week is second. High values (weekend days 5 and 6) push forecasts down.
Low values (early weekdays 0 and 1) push forecasts up. The retailer operates
on a strong weekly cycle with peak activity Monday through Thursday.

rolling_std_14 pushes forecasts negatively when high. High recent revenue
volatility causes the model to reduce its forecast. The model learned to be
conservative during unstable periods because volatility in this dataset
correlates with irregular spikes that do not persist.

lag_1 (yesterday's revenue) ranks 14th of 17. This is counterintuitive but
explained by weekly seasonality. Yesterday was a different day-of-week,
so it is less informative than lag_7, which compares the same weekday last week.

days_since_start captures the gradual baseline shift from 2010 to 2011.
Later dates in the series produce higher baseline forecasts. This feature
was added specifically to provide the model with a monotonic time signal.

## Forecast Quality Assessment
The model tracks the weekly rhythm well across the full 90-day holdout.
Zero-revenue weekend days are correctly anticipated.
Mid-range trading days are estimated within reasonable tolerance.
Spike days (above 75th percentile) are systematically underestimated.
The December 9 peak of £198,095 (44 orders, average basket £4,500) produced
the maximum error of £143,514. No lag or rolling feature could anticipate this.

## Where V1 Is Useful
Operational planning for normal trading days.
Weekly revenue expectations and staffing/inventory planning.
Detection of weeks performing below historical norms.

## Where V1 Is Not Sufficient
Predicting one-off demand shocks from large single customers.
Forecasting peak holiday week revenue accurately.
Any scenario requiring knowledge of promotional activity or external events.

# Forecast Results — V2 Update
---

## V2 Model Results

### V2 Feature Additions Over V1
V2 added the following feature categories to V1's 17-feature base:

Holiday and calendar layer:
- UK public holiday flags
- Pre-holiday window indicators (7 days before major holidays)
- Peak season flag (October through December)
- Month-end window indicator (day 25 onward)
- December indicator

Demand intensity signals:
- Daily active customer count
- Average basket value per day
- Large-order flag (above 95th percentile single-transaction value)
- Revenue and order week-over-week growth rates

Total V2 features: approximately 30-35

### V2 Holdout Performance

All metrics evaluated on 2011-09-11 to 2011-12-09 (90 days).
Same holdout window as V1. No data leakage — holdout defined before
any V2 training began.

| Metric | V1 | V2 | Improvement |
|---|---|---|---|
| MAE | £12,258 | £7,248 | +40.87% |
| RMSE | £20,764 | £15,641 | +24.67% |
| R² | 34.89% | 63.06% | +80.72% |
| WAPE | 24.38% | 14.41% | +40.87% |
| Bias | −8.54% | −9.08% | −6.29% (regression) |
| Spike-Day MAE | £42,755 | £29,408 | +31.22% |

### V2 Operational Metrics

| Metric | Value |
|---|---|
| RMSE | £15,641 |
| MAE | £7,248 |
| WAPE | 14.4% |
| R² Score | 0.631 |
| Peak actual revenue (holdout) | £200,919 (Dec 9 2011) |
| V2 forecast on peak day | £75,438 |
| Peak day absolute error | £125,481 |
| Minimum error day | £16 |

### V2 Top 10 Worst Forecast Days

| Rank | V2 Error | V1 Error | V2 Improvement |
|---|---|---|---|
| 1 | £125,481 | £139,473 | £13,992 better |
| 2 | £28,708 | £52,897 | £24,189 better |
| 3 | £20,864 | £40,163 | £19,299 better |
| 4 | £18,269 | £30,617 | £12,348 better |
| 5 | £17,956 | £29,100 | £11,144 better |
| 6 | £17,168 | £28,871 | £11,703 better |
| 7 | £16,686 | £28,719 | £12,033 better |
| 8 | £15,231 | £26,381 | £11,150 better |
| 9 | £15,115 | £26,338 | £11,223 better |
| 10 | £14,643 | £25,540 | £10,897 better |

V2 improves on every single one of V1's top 10 worst days.
This confirms the improvement is structural, not just average-level.

### WAPE in Industry Context

V2 WAPE of 14.41% meets the professional retail forecasting threshold.
Industry benchmark: WAPE below 15-20% is considered strong performance
for daily grain models without promotional data.
V2 achieves this without external promotional calendars or
competitor/weather data — using only internal transaction history
plus derived demand intensity and calendar signals.

### Forecast Monitoring Summary

Actual vs Predicted trend: V2 tracks the weekly revenue cycle
closely from September through November. Clear alignment visible
across the majority of the 90-day holdout.

December 9 spike: Actual £200,919, V2 forecast £75,438.
Error: £125,481. This remains the dominant error event.
It is visually identifiable as the largest spike in all error charts.

Error distribution: Most holdout days show low absolute error.
The Forecast Error Monitoring timeline is mostly flat near zero
with the December spike as the clear single outlier. This confirms
V2 performs consistently across normal trading days.

### V2 Decision

V2 is selected as the operational forecasting model.
It outperforms V1 on 5 of 6 metrics and meets the WAPE threshold
for professional retail forecasting.

Deployment recommendation: Run V2 in parallel with V1 for 30 days
to validate live performance before full cutover.
Monitor WAPE and MAE weekly against holdout benchmarks.
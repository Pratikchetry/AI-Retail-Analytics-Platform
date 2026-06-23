# V2 Roadmap — Forecasting Improvement Plan

## Why V2 Is Needed

Version 1 established a reliable baseline forecasting system using only
historical transaction behavior from the Online Retail warehouse.

The model successfully learned weekly demand rhythm, weekday-seasonality
patterns, and short-term order momentum. On the 90-day holdout period,
the selected XGBoost model outperformed both naive and classical baselines.

However, dashboard analysis and forecast-error investigation revealed a
critical business limitation: the model consistently underpredicted rare
high-revenue spike days driven by unusually large customer orders.

This insight became visible only after integrating:
- Forecast vs Actual dashboards
- Anomaly detection outputs
- SHAP explainability
- Revenue trend analysis
- Daily operational monitoring in Tableau

The objective of V2 is not to replace V1.
The objective is to reduce the known forecasting weaknesses discovered
during real business analysis.

---

# V1 Performance Summary

| Metric | V1 Result | Business Interpretation |
|---|---|---|
| MAE | 11,805.29 | Average daily forecast miss was approximately £11.8K |
| RMSE | ~21,450 | Large forecast misses still exist on volatile days |
| RMSE improvement vs seasonal naive baseline | 12.6% | XGBoost materially improved forecast stability |
| MAE improvement vs baseline | 21.9% | Better day-to-day operational forecasting |
| Forecast bias | −12% | Model is systematically conservative |
| Max observed error | 143,514 | Extreme spike-day failure remains unresolved |
| Normal-day forecasting | Strong | Weekly demand rhythm captured successfully |
| Spike-day forecasting | Weak | Large individual orders remain difficult to predict |

---

# Business Findings From V1

## What Worked Well

### 1. Weekly Revenue Rhythm Was Learned Successfully

The model learned clear weekly trading behavior:
- Monday–Thursday showed stronger revenue consistency
- Weekend periods produced lower predicted revenue
- Lag-7 features consistently outperformed lag-1 features

Business value:
The system is operationally useful for:
- staffing estimation
- inventory planning
- short-term revenue monitoring
- weekday demand forecasting

---

### 2. Order Momentum Became the Strongest Predictive Signal

SHAP analysis showed:
- `orders_rolling_mean_7`
  was the highest-impact forecasting feature

Interpretation:
Recent order activity predicts future revenue better than
recent revenue alone.

Business meaning:
Demand momentum matters more than isolated daily spikes.

---

### 3. Forecast Stability Improved Over Baselines

Compared with the seasonal naive benchmark:
- RMSE improved by 12.6%
- MAE improved by 21.9%

This confirms:
- feature engineering added measurable forecasting value
- rolling-window features improved signal quality
- XGBoost captured nonlinear demand behavior better than classical models

---

# Core Weakness Discovered in V1

## Extreme Spike Days Were Underpredicted

The largest forecasting failures occurred on days where:
- a small number of customers generated unusually large transactions
- average basket size increased sharply
- revenue spikes appeared without historical precedent

One major spike day reached:
- approximately £198K daily revenue
- driven by only ~44 large orders

The model significantly underforecasted these events.

---

# Why V1 Failed on Spike Days

The issue was not model selection alone.

The real limitation was feature context.

V1 primarily used:
- lag features
- rolling averages
- calendar variables
- order counts
- revenue history

These features explain:
- normal operational demand
- seasonality
- momentum patterns

But they do NOT directly explain:
- sudden enterprise purchasing behavior
- unusually high basket values
- concentrated customer spending
- pre-holiday bulk ordering behavior

As a result:
the model became conservative during volatility.

---

# V1 Architecture Summary

## Selected Forecasting Model

Model:
- XGBoost Regressor

Training strategy:
- Time-series forecasting
- 90-day holdout validation
- Historical feature engineering pipeline

---

# V1 Feature Set

## Revenue Lag Features
- lag_1
- lag_7
- lag_14
- lag_28

## Rolling Revenue Features
- rolling_mean_7
- rolling_mean_14

## Rolling Volatility Features
- rolling_std_7
- rolling_std_14

## Order Activity Features
- orders_lag_1
- orders_lag_7
- orders_rolling_mean_7

## Calendar Features
- day_of_week
- day_of_month
- month
- week_of_year
- is_weekend

## Trend Feature
- days_since_start

Total engineered features:
- 17

---

# V2 Forecasting Strategy

V2 is designed specifically to reduce:
- conservative bias
- spike-day forecasting failures
- extreme prediction error variance

The strategy is NOT:
"change the algorithm and hope."

The strategy is:
add business-aware context.

---

# V2 Planned Improvements

## 1. Holiday and Peak-Season Intelligence

### New Features
- is_uk_public_holiday
- days_to_next_holiday
- days_since_last_holiday
- is_pre_holiday_window
- is_december
- is_peak_season
- is_month_end_window
- is_quarter_end

Business purpose:
Retail demand changes dramatically around:
- holidays
- quarter close
- year-end purchasing periods

V1 had almost no explicit holiday awareness.

---

## 2. Demand Intensity Features

### Planned Features
- daily_active_customers
- avg_basket_value
- large_order_flag
- customer_concentration
- orders_lag_7_growth
- revenue_lag_7_growth

Business purpose:
Spike days are often caused by:
- unusually large baskets
- concentrated enterprise purchasing
- sudden customer-volume acceleration

These signals were absent in V1.

---

## 3. Spike Risk Modeling Layer

### Planned Features
- spike_probability
- anomaly_score_lag_7

Goal:
Estimate whether a day is likely to become:
- high-risk
- highly volatile
- revenue-abnormal

This converts anomaly behavior into forecasting context.

---

# V2 Architecture — Two-Stage Forecasting

## Stage 1 — Baseline Demand Model

Purpose:
Predict normal operational revenue.

Model:
- XGBoost Regressor
- enriched feature set

Output:
Expected revenue under normal business conditions.

---

## Stage 2 — Spike Uplift Layer

Purpose:
Handle rare high-revenue events separately.

Pipeline:
1. Binary spike classifier
2. Spike uplift regressor

Logic:
If spike probability exceeds threshold:
- apply uplift adjustment

Else:
- use baseline forecast only

---

# Why Public Retail Datasets Matter

V2 design is inspired by successful retail forecasting systems such as:
- Rossmann Store Sales
- Walmart forecasting benchmarks

These systems consistently show that:
holiday and external-context features materially improve forecast quality.

Important clarification:
These datasets are NOT merged into the Online Retail II warehouse.

Instead:
their feature-engineering philosophy informs V2 design decisions.

---

# V2 Evaluation Plan

V2 will be evaluated on the SAME 90-day holdout window used in V1.

This ensures:
- fair comparison
- measurable improvement tracking
- reproducible benchmarking

---

# Planned Evaluation Metrics

| Metric | Purpose |
|---|---|
| MAE | Average operational forecasting error |
| RMSE | Sensitivity to large forecast misses |
| WAPE | Revenue-weighted forecasting quality |
| Forecast bias | Detect systematic over/under forecasting |
| Spike-day MAE | Measure high-volatility performance |
| Normal-day MAE | Measure operational consistency |
| Max error | Worst-case business failure analysis |

---

# V2 Success Criteria

V2 will be considered successful if it achieves:

- lower spike-day error
- reduced forecast bias
- improved RMSE stability
- stronger peak-season forecasting
- better handling of abnormal demand behavior

WITHOUT sacrificing:
- normal-day forecast stability
- operational consistency
- interpretability

---

# What V2 Will NOT Claim

V2 will NOT claim:
- perfect forecasting
- complete spike prediction
- 100% accuracy

Retail demand spikes driven by large customer behavior are
structurally difficult to predict from historical data alone.

The goal is not perfection.

The goal is:
- lower risk
- improved stability
- better business awareness
- measurable forecasting improvement
- transparent model limitations

---

# Final Business Conclusion

Version 1 transformed the project from:
"a machine learning notebook"

into:
"a real retail intelligence system."

The most important outcome of V1 was not only improved metrics.

The most important outcome was discovering:
- where the forecasting system succeeds
- where it fails
- why those failures occur
- what business signals are missing
- how Version 2 should evolve

That transition from:
"model training"
to
"business-aware forecasting engineering"

is the foundation of the V2 roadmap.
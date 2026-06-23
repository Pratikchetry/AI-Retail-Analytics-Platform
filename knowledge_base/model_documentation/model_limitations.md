# Model Limitations — V1

This document records known limitations of all V1 models honestly.
These limitations are not failures. They are documented constraints
that inform the V2 design brief.

---

## Forecasting Model (XGBoost V1)

### Limitation 1 — Extreme Spike Day Underestimation
The model cannot predict days driven by a small number of unusually large
individual orders. The December 9 2011 spike produced £198,095 in revenue
from only 44 orders, an average basket of approximately £4,500.
The typical average basket in this dataset is much lower.
No lag feature, rolling average, or calendar feature can anticipate
a day where a handful of customers place unusually large orders.
This produced the maximum absolute error of £143,514.

Root cause: The feature set captures volume momentum and temporal patterns
but has no signal for individual transaction size or customer-level intent.

V2 fix: Add average basket value as a lag feature. Add a large-order-day
flag derived from the 95th percentile of daily maximum transaction size.
Add active customer count per day as a demand breadth signal.

### Limitation 2 — No External Features
The model uses only internal transaction history.
It has no knowledge of public holidays, promotional events, school holidays,
weather, or competitor activity.
Retail forecasting research (Rossmann, Walmart datasets) consistently shows
that promotional and holiday features materially reduce forecast error on
peak days. Public holiday windows in the UK calendar (Christmas, Easter,
bank holidays) are partially captured by the day-of-week and month features
but not explicitly modeled.

V2 fix: Add a UK public holiday flag. Add a pre-holiday window indicator
(7 days before major holidays). Add a December indicator and a peak-season
flag for October through December.

### Limitation 3 — Conservative Bias
Average forecast revenue is £38,592 versus average actual revenue of £43,947.
The model underpredicts by approximately 12% on average across the holdout.
Tree models trained to minimize squared error learn to predict toward the
conditional mean, which dampens predictions toward the center of the
training distribution. Extreme upside days are structurally underweighted.

V2 fix: A second-stage spike uplift model specifically trained on high-revenue
days can provide an additive correction when the first-stage model's
confidence interval suggests a high-revenue day is likely.

### Limitation 4 — Fixed Training Window
The model was trained on a single fixed historical window and not retrained
as new data arrived. In production, a rolling retrain would incorporate
the most recent trading patterns. Without retraining, the model's
representation of current trading levels becomes stale over time.

V2 fix: Design the training pipeline to support periodic retraining
using the most recent 18-24 months of data.

### Limitation 5 — SARIMA Evaluation Method
SARIMA was evaluated using a fixed 90-step-ahead projection from a single
fitted model rather than walk-forward validation. Walk-forward validation
refits or updates the model at each step using newly observed data, which
is more realistic for operational forecasting. The current evaluation
may have penalized SARIMA more than a walk-forward setup would.
This does not change the decision to use XGBoost, but it means the SARIMA
comparison is not perfectly apples-to-apples.

---

## Anomaly Detection (IsolationForest V1)

### Limitation 1 — Uniform Contamination Rate
Contamination is set to 0.05 uniformly across all countries.
This assumes every country has approximately 5% anomalous days.
In reality, a high-volatility market like Germany may have a higher
true anomaly rate, while a stable market may have lower.
Germany's 52% anomaly rate from 38 scored rows suggests the model
is unreliable for borderline-history countries.

V2 fix: Implement adaptive contamination based on each country's
historical volatility, or raise the minimum observations threshold
from 30 to 50 to exclude unstable country models.

### Limitation 2 — Multivariate Unusualness vs Revenue Extremes
IsolationForest detects unusual combinations of all features, not only
revenue extremes. Some flagged days have moderate revenue but unusual
feature combinations such as atypical day-of-week patterns or lag values.
This is statistically correct behavior but can be counterintuitive when
the largest revenue spike in Australia was not flagged while smaller
days were. The model saw the run-up in rolling average before the spike
and scored that day as less isolated in feature space.

V2 fix: Add a revenue-percentile-based rule alongside the model score.
Any day above the 97.5th percentile for its country is automatically
reviewed regardless of isolation score.

### Limitation 3 — No Temporal Context Across Countries
The model scores each country independently with no knowledge of whether
unusual behavior is occurring simultaneously across multiple markets.
A coordinated spike across UK, Germany, and France on the same day is
treated as three independent anomalies, not one cross-market event.

V2 fix: Add a cross-country synchrony signal as a post-processing step.
Days where three or more countries show elevated anomaly scores
simultaneously are flagged as correlated events.

---

## RFM Segmentation

### Limitation 1 — Static Snapshot
RFM segments reflect customer behavior at the time of computation.
They do not update automatically as new transactions occur.
A Champion who stopped buying after the analysis date would still
show as a Champion until the model is rerun.

V2 fix: Design RFM as a scheduled SQL view that recalculates
from the warehouse on a rolling basis rather than a one-time notebook output.

### Limitation 2 — Missing Customer Coverage
24% of transactions (243,007 rows) have no Customer ID.
These transactions contribute to revenue metrics but cannot be
attributed to any customer segment. Anonymous buyer behavior is
structurally excluded from segmentation.

No V2 fix: This is a data collection constraint, not a modeling constraint.
It should be acknowledged in all customer-level reporting.
# Anomaly Detection Findings

## Approach
IsolationForest was applied at the country level, not pooled across all countries.
This is the critical design decision. A pooled model would have UK revenue
volume dominate the contamination budget, flagging almost all anomalies
in UK rows and treating every small-country spike as normal by comparison.
Country-level isolation means each country is evaluated against its own
historical behavioral baseline.

## Input Data
2,893 country-day observations were used as input across 43 countries.
The model required a minimum of 30 observations per country to score it.
Countries with fewer than 30 observations were marked as skipped_low_history
and excluded from the warehouse output.

## Results
Total rows scored: 2,639
Rows skipped due to insufficient history: 171
Countries scored: 18 out of 43
Total anomalies detected: 139
High anomalies (positive revenue spikes): 117 (84.17% of all anomalies)
Low anomalies (demand collapses or unusual drops): 22 (15.83%)

## Contamination Parameter
Contamination was set to 0.05, meaning the model assumes approximately
5% of country-day observations are anomalous. This is a modeling assumption,
not a data-derived threshold. The actual anomaly rate in the scored data
is 139 divided by 2639, which equals 5.27%, consistent with this setting.

## Country Distribution of Anomalies
United Kingdom: 31 anomalies (highest count, expected given largest market)
Germany: 20 anomalies
France: 17 anomalies
EIRE: 17 anomalies
Netherlands: 8 anomalies
Spain: 7 anomalies
Belgium: 7 anomalies
Switzerland: 4 anomalies
Sweden: 4 anomalies
Portugal: 4 anomalies
Australia: 4 anomalies
Italy: 3 anomalies
Finland: 3 anomalies
Norway: 2 anomalies
Denmark: 2 anomalies
Cyprus: 2 anomalies
Channel Islands: 2 anomalies
Austria: 2 anomalies

## Key Business Interpretations
84% of anomalies are positive demand spikes, not revenue collapses.
This means unusual behavior in this retailer is driven by sudden large orders
rather than widespread operational failures or demand drops.
The anomaly distribution across 18 countries rather than concentration in UK
confirms the country-level approach is working correctly.
Germany has 20 anomalies from 38 scored rows, which is a 52% anomaly rate.
This is unusually high and suggests Germany may have had borderline
observation count. Results for Germany should be interpreted with caution.

## Features Used
day_of_week, month, revenue_lag1 (previous day revenue),
revenue_rolling7 (7-period rolling average), daily_revenue, daily_orders.

## Anomaly Direction Classification
An anomaly_direction field was added to the warehouse output:
high means the anomalous day had revenue above the country median.
low means the anomalous day had revenue below the country median.
normal means the row was not flagged as anomalous.
This field enables dashboards to distinguish demand spikes from demand drops.

## Known Limitations
Germany anomaly rate of 52% warrants investigation. A higher minimum
observations threshold of 50 rather than 30 would likely produce more
stable results for borderline countries.
The contamination rate of 0.05 is applied uniformly. Adaptive contamination
per country based on observed variance would be more precise.
IsolationForest detects multivariate unusualness, not just revenue extremes.
Some flagged days have moderate revenue but unusual feature combinations
such as abnormal day-of-week or lag patterns. This is correct behavior
but requires explanation when reviewing specific anomaly flags.
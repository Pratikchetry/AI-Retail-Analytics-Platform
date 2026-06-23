# EDA Findings — Retail Revenue Intelligence

## Dataset Overview
The Online Retail II dataset contains wholesale transaction data from a
UK-based retailer. The full period runs from December 1 2009 to December 9 2011.
After cleaning, 1,007,914 valid sales rows remain from an original 1,067,371.

## Revenue Summary
Total validated revenue is £20,476,634.
Merchandise-only revenue is £19,701,497.66.
The gap of £775,136 represents postage, service charges, and manual adjustments.
Total distinct orders: 40,078 across the full period.

## Geographic Concentration
The United Kingdom generates £17,410,570, which is 85% of all revenue.
EIRE is second at £658,767 (3.2%).
Netherlands is third at £554,038 (2.7%).
Germany is fourth at £425,020 (2.1%).
France is fifth at £350,456 (1.7%).
All remaining 38 countries combined contribute approximately 5.3% of revenue.

Business implication: Overall revenue performance, forecasting behavior,
and anomaly patterns are driven primarily by UK market dynamics. Any
global revenue metric is effectively a UK metric with international noise.
All dashboards should offer UK versus Non-UK segmentation as a primary filter.

## Seasonality
Revenue shows clear late-year seasonal peaks in October through December.
STL decomposition on the training series confirmed strong weekly seasonality
with a period of 7 days. The trend component shows a minimum of negative 347
and a maximum of 50,113, confirming the series is not flat.
The seasonal component ranges from negative 45,327 to positive 43,216,
which is very strong relative to the typical daily revenue level.
Residual standard deviation is 10,051, meaning significant irregular
variation remains after removing trend and weekly seasonality.

## Customer Concentration
5,878 customers were segmented using RFM scoring.
The top segment, Champions, contains 1,268 customers (21.6% of the base)
and generates 67.89% of total revenue.
Champion average spend is £9,302 with an average of 17 purchases.
Champions last purchased an average of 19 days ago.
Lost customers average spend is only £343 with 1 purchase and 568 days
since last transaction.
At Risk High Value customers have average spend of £3,625 but have not
purchased in an average of 366 days, making them the highest-priority
reactivation target.

## Non-Merchandise Revenue
Certain stock codes do not represent physical merchandise.
These include POST (postage), DOT (DOTCOM postage), M (manual entries),
BANK CHARGES, AMAZONFEE, and SAMPLES.
These codes are flagged with is_merchandise equals FALSE in dim_product.
Revenue totals that include these codes overstate product demand by approximately
£775,136 over the full period.
All forecasting uses merchandise revenue as the primary target.
All product rankings filter to is_merchandise equals TRUE.

## Missing Customer ID
243,007 rows have no Customer ID, representing approximately 24% of transactions.
These rows are included in revenue and order metrics but excluded from
customer segmentation. They are assigned a surrogate Unknown Customer key
in the warehouse rather than being silently dropped.

## Data Quality Issues Found in Profiling
34,335 exact duplicate rows were identified and removed.
22,950 negative Quantity rows were separated as returns and cancellations.
5 negative Price rows were separated as accounting adjustments.
4,382 rows had missing Description values.
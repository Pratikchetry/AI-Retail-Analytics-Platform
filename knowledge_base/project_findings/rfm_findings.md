# RFM Segmentation Findings

## What RFM Measures
RFM stands for Recency, Frequency, and Monetary value.
Recency measures how recently a customer last made a purchase.
Frequency measures how many times a customer has purchased.
Monetary measures how much a customer has spent in total.
Each customer is scored on all three dimensions and grouped into behavioral segments.

## Segmentation Results
Total customers segmented: 5,878
Customers excluded due to missing Customer ID: approximately 243,007 transactions
had no customer identifier and could not be attributed to any segment.

## Segment Detail

### Champions — 1,268 customers
Revenue contribution: £11,795,212
Revenue share: 67.89% of total segmented revenue
Average spend: £9,302
Average purchase frequency: 17 orders
Average days since last purchase: 19
These customers buy frequently, buy a lot, and bought recently.
They are the foundation of the business.

### Loyal Customers — 1,423 customers
Revenue contribution: £2,709,526
Average spend: £1,904
Average frequency: 5 orders
Average days since last purchase: 71
High frequency buyers who are still active but spend less per transaction.

### At Risk — High Value — 453 customers
Revenue contribution: £1,428,405
Average spend: £3,625
Average frequency: 6 orders
Average days since last purchase: 366
These customers historically spent large amounts and bought frequently
but have not returned in over a year. This is the highest-priority
reactivation segment because their historical value is high.

### Potential Loyalists — 394 customers
Average spend: £408
Average frequency: 1 order
Average days since last purchase: 320
Recent new buyers with potential to develop into loyal customers
if re-engaged quickly.

### New Customers — 476 customers
Average spend: £908
Average frequency: 1 order
Average days since last purchase: 27
Very recently acquired customers who have made one purchase.
Priority is to encourage a second purchase.

### At Risk — Frequent — 516 customers
Average spend: £615
Average frequency: 3 orders
Average days since last purchase: 382
Customers who bought multiple times but have gone quiet.
Lower monetary value than At Risk High Value but meaningful frequency history.

### Lost — 1,348 customers
Revenue contribution: £163,148
Average spend: £343
Average frequency: 1 order
Average days since last purchase: 568
Customers who bought once a long time ago and never returned.
Lowest reactivation priority.

## Key Business Interpretations
Losing one Champion customer has roughly the same revenue impact as
losing 27 Lost-segment customers.
The At Risk High Value segment (453 customers, £3,625 average spend,
not seen in 366 days) represents approximately £1.6M in annualized
revenue at risk if these customers do not return.
New Customers (476 customers) are the conversion opportunity.
A second purchase converts a new customer toward the Loyal segment.
Champions have 17 average purchases compared to 1 for Lost and New customers,
confirming that frequency is the strongest differentiator of high-value behavior.

## Methodology Notes
RFM scores were computed from the validated fact_sales table in PostgreSQL.
Customers with missing Customer ID were excluded entirely.
Segments were defined using quantile-based scoring rather than fixed thresholds.
Results are stored in ml_rfm_segments in the warehouse.

# RFM Findings — V2 Update
---

## V2 Customer Segmentation Results

The V2 customer dashboards replaced the V1 RFM segment definitions
with a revised scoring approach. The corrected dashboard now shows
Champions with the highest monetary value, highest frequency, and
lowest recency days — consistent with standard RFM behavioral theory.
An earlier version had inverted segment labels which has been corrected.

---

## V2 Segment Distribution

Total customers segmented: 5,878 (same base as V1)

| Segment | Customer Count | % of Base |
|---|---|---|
| At Risk | 1,411 | 24.0% |
| Loyal Customers | 1,341 | 22.8% |
| Champions | 1,317 | 22.4% |
| Potential Loyalists | 968 | 16.5% |
| Lost Customers | 841 | 14.3% |

---

## V2 Average Monetary Value by Segment

| Segment | Avg Monetary Value | Rank |
|---|---|---|
| Champions | £9,552 | 1st — highest |
| Loyal Customers | £2,298 | 2nd |
| Potential Loyalists | £907 | 3rd |
| At Risk | £475 | 4th |
| Lost Customers | £198 | 5th — lowest |

Champions generate 48x more average value than Lost Customers.
Champions generate 4.2x more average value than Loyal Customers.
This concentration confirms the business is heavily dependent on
a small number of high-value repeat buyers.

---

## V2 Average Purchase Frequency by Segment

| Segment | Avg Purchases | Rank |
|---|---|---|
| Champions | 17.71 | 1st — highest |
| Loyal Customers | 5.58 | 2nd |
| Potential Loyalists | 3.00 | 3rd |
| At Risk | 1.69 | 4th |
| Lost Customers | 1.04 | 5th — lowest |

Champions purchase 17x more frequently than Lost Customers.
The gap between Champions (17.71) and Loyal Customers (5.58)
is 3.2x — a meaningful behavioral difference within active segments.
Potential Loyalists at 3.00 purchases show genuine repeat behavior
and represent the conversion opportunity to the Loyal tier.

---

## V2 Average Recency (Days Since Last Purchase)

| Segment | Avg Days Inactive | Risk Classification |
|---|---|---|
| Champions | 25.1 | Active — very low risk |
| Loyal Customers | 100.0 | Stable — low risk |
| Potential Loyalists | 173.1 | Drifting — medium risk |
| At Risk | 292.6 | High risk — urgent |
| Lost Customers | 515.0 | Critical — permanent churn risk |

---

## Customer Retention Action Matrix

| Segment | Recommended Action | Priority Level |
|---|---|---|
| At Risk | Immediate Re-engagement | Priority (red) — urgent |
| Loyal Customers | Loyalty Programs | Core play (green) — maintain |
| Champions | Reward & Retain | VIP (blue) — protect |
| Potential Loyalists | Upsell & Nurture | Grow (purple) — develop |
| Lost Customers | Win-back Campaign | Re-activate (black) — low cost |

---

## V2 Key Business Findings

### Finding 1 — Champions Are the Revenue Foundation
1,317 Champions generate £9,552 average value, purchase 17.71 times,
and bought as recently as 25.1 days ago on average.
This is the highest-value, most-engaged, most-recent segment.
Retention and VIP treatment is the correct strategy.
Any churn from this segment has immediate and significant revenue impact.

### Finding 2 — At Risk Is the Largest Segment and Highest Volume Risk
1,411 customers are at risk — the largest segment by count.
At 292.6 days average inactivity, these customers are approaching
the 300-day threshold beyond which reactivation probability drops
significantly. At £475 average value and 1.69 purchases, individual
contribution is moderate but the volume makes this the highest
collective churn risk.
Immediate re-engagement campaigns are the correct action.
Each day of delay reduces reactivation probability.

### Finding 3 — Lost Customers Are Borderline Recoverable
841 customers with 515 days average absence and £198 average value.
A 515-day absence means most of these customers last purchased
in late 2009 to mid 2010. A targeted win-back campaign is appropriate
but should use low-cost automated channels only.
High-touch outreach for £198 average customers is not cost-effective.

### Finding 4 — Potential Loyalists Are the Development Opportunity
968 customers with 3.00 average purchases, £907 average value,
and 173.1 days since last purchase.
These customers have demonstrated genuine repeat behavior but
are drifting toward At Risk territory. The window to convert
them to Loyal Customers is open but narrowing.
Upsell and nurture campaigns targeting this segment specifically
can protect the transition before they cross 300 days of inactivity.

### Finding 5 — Loyal Customers Are Stable but Not Growing
1,341 customers with 5.58 purchases, £2,298 average value,
100 days since last purchase.
This is the stable revenue middle tier — reliably active but
not generating Champions-level value.
Loyalty programme investment maintains this segment without
requiring intensive intervention.

---

## V1 vs V2 Segmentation Comparison

The V1 and V2 segmentation used different thresholds and produced
different segment distributions. Direct segment-by-segment count
comparison is not valid because the scoring boundaries changed.

What is comparable is the behavioral pattern per segment.
Both V1 and V2 confirm the same core finding: the top segment
generates disproportionate revenue (V1 Champions: £9,302 avg,
V2 Champions: £9,552 avg) while the bottom segments have
near-zero individual value.

The V2 customer count distribution is more even across segments
(1,411 / 1,341 / 1,317 / 968 / 841) compared to V1's
more skewed distribution. This suggests the V2 thresholds
produce a more balanced segmentation that may be more
operationally useful for targeted campaign planning.

---

## Data Quality Note — Correction Record

An earlier version of the V2 customer dashboard had inverted
RFM segment labels. Potential Loyalists were incorrectly showing
the highest monetary value (£8,115) and frequency (15.64) while
Champions showed the lowest values. This indicated the recency
score was ranked in the wrong direction during computation.

The corrected version (current) shows:
- Champions: £9,552 value, 17.71 frequency, 25.1 days recency ✓
- Lost Customers: £198 value, 1.04 frequency, 515.0 days recency ✓

This is the correct behavioral ordering and matches standard
RFM theory. All documentation uses the corrected numbers.
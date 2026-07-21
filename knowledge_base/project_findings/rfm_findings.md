## RFM Segmentation Findings
### What RFM Measures
RFM stands for Recency, Frequency, and Monetary value.Recency measures how recently a customer last made a purchase.Frequency measures how many times a customer has purchased.Monetary measures how much a customer has spent in total.Each customer is scored on all three dimensions and grouped into behavioral segments.

### Segmentation Results
Total customers segmented: 5,878Customers excluded due to missing Customer ID: approximately 243,007 transactionshad no customer identifier and could not be attributed to any segment.

### Segment Detail
Champions — 1,317 customers
Average spend: £9,552Average purchase frequency: 17.71 ordersAverage days since last purchase: 25.1These customers buy frequently, buy a lot, and bought recently.They are the foundation of the business.

### Loyal Customers — 1,341 customers
Average spend: £2,298Average frequency: 5.58 ordersAverage days since last purchase: 100.0High frequency buyers who are still active but spend less per transaction.

### At Risk — 1,411 customers
Average spend: £475Average frequency: 1.69 ordersAverage days since last purchase: 292.6These customers historically spent large amounts and bought frequentlybut have not returned in over a year. This is the highest-priorityreactivation segment because their historical value is high.

### Potential Loyalists — 968 customers
Average spend: £907Average frequency: 3.00 ordersAverage days since last purchase: 173.1Recent new buyers with potential to develop into loyal customersif re-engaged quickly.

### Lost Customers — 841 customers
Average spend: £198Average frequency: 1.04 ordersAverage days since last purchase: 515.0Customers who bought once a long time ago and never returned.Lowest reactivation priority.

### Key Business Interpretations
Losing one Champion customer has roughly the same revenue impact aslosing 27 Lost-segment customers.The At Risk segment (1,411 customers, £475 average spend,not seen in 292.6 days) represents the highest collective churn risk.Potential Loyalists (968 customers) are the conversion opportunity.A third purchase converts a potential loyalist toward the Loyal segment.Champions have 17.71 average purchases compared to 1.04 for Lost customers,confirming that frequency is the strongest differentiator of high-value behavior.

### Methodology Notes
RFM scores were computed from the validated fact_sales table in PostgreSQL.Customers with missing Customer ID were excluded entirely.Segments were defined using quantile-based scoring rather than fixed thresholds.Results are stored in ml_rfm_segments in the warehouse.

### RFM Findings — V2 Update
#### V2 Customer Segmentation Results
The V2 customer dashboards replaced the V1 RFM segment definitionswith a revised scoring approach. The corrected dashboard now showsChampions with the highest monetary value, highest frequency, andlowest recency days — consistent with standard RFM behavioral theory.An earlier version had inverted segment labels which has been corrected.

### V2 Segment Distribution
Total customers segmented: 5,878 (same base as V1)

Segment	Customer Count	% of Base
At Risk	1,411	24.0%
Loyal Customers	1,341	22.8%
Champions	1,317	22.4%
Potential Loyalists	968	16.5%
Lost Customers	841	14.3%

### V2 Average Monetary Value by Segment
Segment	Avg Monetary Value	Rank
Champions	£9,552	1st — highest
Loyal Customers	£2,298	2nd
Potential Loyalists	£907	3rd
At Risk	£475	4th
Lost Customers	£198	5th — lowest

Champions generate 48x more average value than Lost Customers.Champions generate 4.2x more average value than Loyal Customers.This concentration confirms the business is heavily dependent ona small number of high-value repeat buyers.

### V2 Average Purchase Frequency by Segment
Segment 	Avg Purchases 	Rank
Champions	17.71	1st — highest
Loyal Customers	5.58	2nd
Potential Loyalists	3.00	3rd
At Risk	1.69	4th
Lost Customers	1.04	5th — lowest

Champions purchase 17x more frequently than Lost Customers.The gap between Champions (17.71) and Loyal Customers (5.58)is 3.2x — a meaningful behavioral difference within active segments.Potential Loyalists at 3.00 purchases show genuine repeat behaviorand represent the conversion opportunity to the Loyal tier.

### V2 Average Recency (Days Since Last Purchase)
Segment  Avg Days Inactive 	Risk Classification 
Champions	25.1	Active — very low risk
Loyal Customers	100.0	Stable — low risk
Potential Loyalists	173.1	Drifting — medium risk
At Risk	292.6	High risk — urgent
Lost Customers	515.0	Critical — permanent churn risk

### Customer Retention Action Matrix
Segment	Recommended Action	Priority Level
At Risk	Immediate Re-engagement	Priority (red) — urgent
Loyal Customers	Loyalty Programs	Core play (green) — maintain
Champions	Reward & Retain	VIP (blue) — protect
Potential Loyalists	Upsell & Nurture	Grow (purple) — develop
Lost Customers	Win-back Campaign	Re-activate (black) — low cost

### V2 Key Business Findings
- Finding 1 — Champions Are the Revenue Foundation
1,317 Champions generate £9,552 average value, purchase 17.71 times,and bought as recently as 25.1 days ago on average.This is the highest-value, most-engaged, most-recent segment.Retention and VIP treatment is the correct strategy.Any churn from this segment has immediate and significant revenue impact.

- Finding 2 — At Risk Is the Largest Segment and Highest Volume Risk
1,411 customers are at risk — the largest segment by count.At 292.6 days average inactivity, these customers are approachingthe 300-day threshold beyond which reactivation probability dropssignificantly. At £475 average value and 1.69 purchases, individualcontribution is moderate but the volume makes this the highestcollective churn risk.Immediate re-engagement campaigns are the correct action.Each day of delay reduces reactivation probability.

- Finding 3 — Lost Customers Are Borderline Recoverable
841 customers with 515 days average absence and £198 average value.A 515-day absence means most of these customers last purchasedin late 2009 to mid 2010. A targeted win-back campaign is appropriatebut should use low-cost automated channels only.High-touch outreach for £198 average customers is not cost-effective.

- Finding 4 — Potential Loyalists Are the Development Opportunity
968 customers with 3.00 average purchases, £907 average value,and 173.1 days since last purchase.These customers have demonstrated genuine repeat behavior butare drifting toward At Risk territory. The window to convertthem to Loyal Customers is open but narrowing.Upsell and nurture campaigns targeting this segment specificallycan protect the transition before they cross 300 days of inactivity.

- Finding 5 — Loyal Customers Are Stable but Not Growing
1,341 customers with 5.58 purchases, £2,298 average value,100 days since last purchase.This is the stable revenue middle tier — reliably active butnot generating Champions-level value.Loyalty programme investment maintains this segment withoutrequiring intensive intervention.
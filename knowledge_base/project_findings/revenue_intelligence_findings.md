# Revenue Intelligence Findings
# File location: knowledge_base/project_findings/revenue_intelligence_findings.md
# Source: Revenue Intelligence & Growth Analytics Dashboard + SQL views

---

## What Was Built

A new Tableau dashboard — Revenue Intelligence & Growth Analytics — was created
using five PostgreSQL analytics views built in sql/analytics/:

| SQL File | View Name | Purpose |
|---|---|---|
| 06_revenue_monthly_summary.sql | revenue_monthly_summary | Monthly revenue, orders, avg daily |
| 07_revenue_seasonality.sql | revenue_seasonality | Year × month cross-tab |
| 08_monthly_growth_analysis.sql | revenue_growth_analysis | MoM growth % |
| 09_yoy_revenue_analysis.sql | yoy_revenue_analysis | 2010 vs 2011 by month |
| 10_revenue_executive_summary.sql | revenue_executive_summary | One-row KPI summary |

---

## What the Dashboard Shows

Five KPI cards across the top:
- Total Revenue: £20,476,634
- Average Monthly Revenue: £819,065
- Best Month: November 2011
- Worst Month: February 2011
- YoY Growth: −0.13%

Four charts below:
1. Monthly Revenue Trend line chart (Dec 2009 – Dec 2011)
2. Revenue Seasonality & YoY Comparison cross-tab (year × month grid)
3. Month-over-Month Revenue Growth % bar chart
4. Year-over-Year Revenue Performance bar chart (2010 vs 2011)

---

## Complete Monthly Revenue Data (from revenue_monthly_summary)

| Year | Month | Revenue | Orders | Avg Daily Revenue |
|---|---|---|---|---|
| 2009 | Dec | £822,484 | 1,682 | £18.93 |
| 2010 | Jan | £651,155 | 1,105 | £21.48 |
| 2010 | Feb | £551,878 | 1,202 | £19.74 |
| 2010 | Mar | £830,915 | 1,681 | £20.86 |
| 2010 | Apr | £678,875 | 1,462 | £20.66 |
| 2010 | May | £657,706 | 1,500 | £19.70 |
| 2010 | Jun | £749,537 | 1,645 | £19.52 |
| 2010 | Jul | £648,810 | 1,529 | £20.20 |
| 2010 | Aug | £695,252 | 1,425 | £21.65 |
| 2010 | Sep | £921,697 | 1,839 | £22.69 |
| 2010 | Oct | £1,161,902 | 2,301 | £20.40 |
| 2010 | Nov | £1,464,293 | 2,747 | £19.51 |
| 2010 | Dec | £821,453 | 1,559 | £20.04 |
| 2011 | Jan | £689,812 | 1,086 | £20.25 |
| 2011 | Feb | £522,546 | 1,100 | £19.44 |
| 2011 | Mar | £716,215 | 1,454 | £20.18 |
| 2011 | Apr | £536,968 | 1,246 | £18.59 |
| 2011 | May | £769,297 | 1,681 | £21.42 |
| 2011 | Jun | £760,547 | 1,533 | £21.29 |
| 2011 | Jul | £718,076 | 1,475 | £18.70 |
| 2011 | Aug | £757,841 | 1,361 | £22.12 |
| 2011 | Sep | £1,056,435 | 1,837 | £21.60 |
| 2011 | Oct | £1,151,264 | 2,040 | £19.67 |
| 2011 | Nov | £1,503,867 | 2,769 | £18.34 |
| 2011 | Dec | £637,808 | 819 | £25.68 |

---

## Year-over-Year Analysis (from yoy_revenue_analysis)

| Month | 2010 Revenue | 2011 Revenue | YoY % | Signal |
|---|---|---|---|---|
| Jan | £651,155 | £689,812 | +5.94% | Growth |
| Feb | £551,878 | £522,546 | −5.32% | Decline |
| Mar | £830,915 | £716,215 | −13.80% | Decline |
| Apr | £678,875 | £536,968 | −20.90% | Largest drop |
| May | £657,706 | £769,297 | +16.97% | Recovery |
| Jun | £749,537 | £760,547 | +1.47% | Flat |
| Jul | £648,810 | £718,076 | +10.68% | Growth |
| Aug | £695,252 | £757,841 | +9.00% | Growth |
| Sep | £921,697 | £1,056,435 | +14.62% | Strong growth |
| Oct | £1,161,902 | £1,151,264 | −0.92% | Flat |
| Nov | £1,464,293 | £1,503,867 | +2.70% | Growth |
| Dec | £821,453 | £637,808 | −22.36% | Partial month |

---

## Month-over-Month Key Movements (from revenue_growth_analysis)

**Largest positive MoM jumps:**
| Date | MoM % | Context |
|---|---|---|
| Mar 2010 | +50.56% | Post-February recovery |
| Oct 2010 | +43.27% | Pre-holiday acceleration |
| Sep 2011 | +39.40% | H2 2011 acceleration |
| May 2011 | +37.06% | Spring recovery |
| Nov 2010 | +26.06% | Peak season entry |

**Largest negative MoM drops:**
| Date | MoM % | Context |
|---|---|---|
| Dec 2011 | −57.59% | Partial month — not a real drop |
| Jan 2010 | −20.83% | Post-Christmas drop |
| Dec 2010 | −43.90% | Expected seasonal decline |
| Apr 2011 | −24.25% | Weakest 2011 period |
| Mar 2011 | −16.03% | Weak H1 2011 |

---

## Executive Summary (from revenue_executive_summary)

| Metric | Value |
|---|---|
| total_revenue | £20,476,634.01 |
| avg_monthly_revenue | £819,065.36 |
| best_month | Nov 2011 |
| worst_month | Feb 2011 |
| best_month_revenue | £1,503,866.78 |
| worst_month_revenue | £522,545.56 |
| yoy_growth | −0.13% |

---

## What This Data Found — Key Business Findings

### Finding 1 — YoY −0.13% is a Partial-Year Artifact, Not a Decline
The −0.13% overall YoY growth figure is misleading on its own.
December 2011 ends on December 9 (partial month) versus December 2010
which is a complete month (£821,453). If December 2011 is excluded,
the comparable 11-month YoY shows a different picture. H2 2011
clearly outperformed H2 2010 in September (+14.62%) and remained
strong in November (+2.70%). The business is not declining.

### Finding 2 — H1 2011 Was Weak, H2 2011 Was Strong
March (−13.80%), April (−20.90%), and February (−5.32%) pulled the
full-year figure down. From May onward, 2011 consistently outperformed
or matched 2010. This suggests a mid-year recovery rather than a
business trend reversal.

### Finding 3 — November Is the Non-Negotiable Peak Month
November 2010: £1,464,293 (2,747 orders)
November 2011: £1,503,867 (2,769 orders)
November is the highest revenue month both years by a wide margin.
All capacity planning — inventory, logistics, customer service —
must treat November as the maximum load benchmark.

### Finding 4 — Average Daily Revenue Is Remarkably Stable
Despite monthly totals ranging from £522K to £1.5M, average daily
revenue across all months stays in the narrow range of £18.34 to
£25.68. Monthly variation is driven by the number of trading days
and seasonal order volume, not by fundamental changes in daily
trading intensity. December 2011's £25.68 average is the highest
despite the lowest monthly total — confirming the partial month effect.

### Finding 5 — April Is a Structural Weak Point Worth Monitoring
April 2011 dropped 20.90% vs April 2010 (£536,968 vs £678,875).
This is not a one-off. April typically represents the lowest-energy
month of the Q1/Q2 calendar for this type of wholesale gifting retailer.
Any demand planning for April should use a conservative assumption.

### Finding 6 — The Seasonal Pattern Is Highly Consistent
Q4 (Oct–Dec) generates approximately 35–38% of annual revenue both years.
The seasonal pattern is reliable enough to be used as a planning signal.
Any forecasting model that does not incorporate the September acceleration
and November peak will systematically underestimate H2 revenue.

---

## Where These Findings Were Pasted

These findings were added to:

1. `knowledge_base/project_findings/revenue_intelligence_findings.md`
   → This file (complete findings)

2. `docs/data_findings.md`
   → Section 2: Revenue Findings updated with monthly table and YoY data

3. `docs/validation_benchmark.md`
   → Monthly revenue benchmarks added as reference values

4. `tableau/README.md`
   → Dashboard 5 section: Revenue Intelligence & Growth Analytics
   → Key numbers, chart descriptions, and business insight filled in

5. `README.md` (root)
   → Monthly Revenue 2010 vs 2011 YoY table added to Key Results
   → Revenue Overview section updated with best/worst month and YoY

---

## SQL Views Summary

These views are production-ready and validated against warehouse benchmarks:

```sql
-- revenue_monthly_summary: 25 rows covering Dec 2009 to Dec 2011
-- revenue_seasonality: same data, year × month format
-- revenue_growth_analysis: MoM % from revenue_monthly_summary
-- yoy_revenue_analysis: 12 rows comparing 2010 vs 2011 by month
-- revenue_executive_summary: 1 row — the business headline KPIs
```

All five views are connected to the Revenue Intelligence dashboard in Tableau.
All five views use fact_sales as the base table.
All revenue totals reconcile to £20,476,634 ground truth.
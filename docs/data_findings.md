# Data Findings Update — New Sections
# Append these sections to the bottom of docs/data_findings.md

---

## 9. Monthly Revenue Pattern

Confirmed from revenue_monthly_summary and revenue_seasonality views.

| Best month | November 2011 — £1,503,867 |
| Worst month | February 2011 — £522,546 |
| Average monthly revenue | £819,065 |
| YoY growth (2010 vs 2011) | −0.13% |

The −0.13% YoY figure is driven by partial December 2011 data and
a weak H1 2011. H2 2011 outperformed H2 2010 in September (+14.62%).
The business is not in decline. The seasonal pattern is consistent
across both years with Q4 generating approximately 35–38% of revenue.

**Peak months consistently:** October, November
**Weak months consistently:** February, April
**Seasonal pattern:** Strong acceleration from September onward each year

---

## 10. Product Revenue Concentration

Confirmed from product_revenue_analysis and product_revenue_contribution views.

Top product: REGENCY CAKESTAND 3 TIER at £330,590 (1.68% of total revenue)
Top 10 products combined: approximately 8.35% of total revenue
Remaining 91.65% distributed across hundreds of other products

Revenue is highly diversified. No single product creates material
single-product concentration risk.

### Critical Product Anomaly
PAPER CRAFT, LITTLE BIRDIE: £168,470 revenue from exactly 1 order.
This is a single wholesale bulk purchase event, not organic recurring demand.
It must be excluded from trend analysis, demand forecasting, and any
product performance conclusions.

---

## 11. Product Volume Pattern

Confirmed from product_quantity_analysis view.

Highest volume product: WORLD WAR 2 GLIDERS ASSTD DESIGNS — 106,139 units
Revenue of top volume product: only £24,446 (£0.23 per unit)

Revenue leaders and volume leaders are entirely different products.
The performance matrix is required to identify products that
perform strongly on both dimensions simultaneously.

Only CREAM HANGING HEART T-LIGHT HOLDER (£257,725 revenue, 94,203 units)
ranks in the top 4 on both revenue AND quantity. It is the only
confirmed Superstar product in the full catalog.

---

## 12. Product Investment Classification

Confirmed from product_investment_analysis view.

| Strategy | Count | % of Catalog |
|---|---|---|
| Monitor | 3,172 | 67.1% |
| Invest More | 810 | 17.1% |
| Premium Focus | 371 | 7.9% |
| Marketing Opportunity | 371 | 7.9% |

67% Monitor status is expected and normal for a wholesale gifting catalog
of this size. The 810 Invest More and 371 Premium Focus products represent
the active commercial portfolio requiring inventory and marketing decisions.

---

## 13. Month-over-Month Growth Key Movements

Confirmed from revenue_growth_analysis view.

Largest positive MoM jumps:
- March 2010: +50.56%
- September 2011: +39.40%
- October 2010: +43.27%

Largest negative MoM drops:
- December 2011: −57.59% (partial month — not a real business drop)
- January 2010: −20.83% (post-Christmas expected)
- April 2011: −24.25%

December 2011 MoM figure is the most misleading number in the dataset.
It should never be used in isolation without the partial-month context.
# Product Intelligence Findings
# File location: knowledge_base/project_findings/product_intelligence_findings.md
# Source: Product Intelligence & Investment Strategy Dashboard + SQL views

---

## What Was Built

A new two-page Tableau dashboard — Product Intelligence & Investment Strategy —
was created using five PostgreSQL analytics views built in sql/analytics/:

| SQL File | View Name | Purpose |
|---|---|---|
| 11_product_revenue_analysis.sql | product_revenue_analysis | Revenue and quantity per product |
| 12_product_quantity_analysis.sql | product_quantity_analysis | Sorted by quantity |
| 13_product_revenue_contribution.sql | product_revenue_contribution | % contribution per product |
| 14_product_performance_matrix.sql | product_performance_matrix | Revenue + quantity + orders combined |
| 15_product_investment_analysis.sql | product_investment_analysis | Investment strategy classification |

---

## Dashboard Page 1 — What It Shows

Three charts:
1. Top Revenue Generating Products — top 10 bar chart by total revenue
2. Top Selling Products by Quantity — top 10 bar chart by total quantity
3. Product Investment Strategy — 4-category distribution bar chart

---

## Top 10 Products by Revenue (from product_revenue_analysis)

| Rank | Product | Revenue | Orders |
|---|---|---|---|
| 1 | REGENCY CAKESTAND 3 TIER | £330,590 | 3,918 |
| 2 | WHITE HANGING HEART T-LIGHT HOLDER | £257,725 | 5,365 |
| 3 | JUMBO BAG RED RETROSPOT | £182,681 | 4,013 |
| 4 | PAPER CRAFT, LITTLE BIRDIE | £168,470 | 1 |
| 5 | PARTY BUNTING | £148,318 | 2,674 |
| 6 | ASSORTED COLOUR BIRD ORNAMENT | £129,324 | 2,807 |
| 7 | PAPER CHAIN KIT 50'S CHRISTMAS | £117,760 | 2,018 |
| 8 | MEDIUM CERAMIC TOP STORAGE JAR | £81,701 | 247 |
| 9 | CHILLI LIGHTS | £80,541 | 1,135 |
| 10 | POPCORN HOLDER | £79,520 | 2,322 |

---

## Top 10 Products by Quantity (from product_quantity_analysis)

| Rank | Product | Quantity | Revenue |
|---|---|---|---|
| 1 | WORLD WAR 2 GLIDERS ASSTD DESIGNS | 106,139 | £24,446 |
| 2 | JUMBO BAG RED RETROSPOT | 96,757 | £180,569 |
| 3 | PACK OF 72 RETRO SPOT CAKE CASES | 94,884 | £51,825 |
| 4 | WHITE HANGING HEART T-LIGHT HOLDER | 94,203 | £257,725 |
| 5 | POPCORN HOLDER | 88,499 | £79,520 |
| 6 | PAPER CRAFT, LITTLE BIRDIE | 80,995 | £168,470 |
| 7 | ASSORTED COLOUR BIRD ORNAMENT | 80,082 | £129,324 |
| 8 | MEDIUM CERAMIC TOP STORAGE JAR | 78,033 | £81,701 |
| 9 | BROCADE RING PURSE | 70,369 | £14,766 |
| 10 | PACK OF 60 PINK PAISLEY CAKE CASES | 56,061 | £28,082 |

---

## Product Investment Strategy Distribution (from product_investment_analysis)

| Strategy | Product Count | Definition |
|---|---|---|
| Monitor | 3,172 | Low to mid performance — watch for trends |
| Invest More | 810 | Strong consistent performance — increase stock and marketing |
| Premium Focus | 371 | High value per unit, lower volume — premium positioning |
| Marketing Opportunity | 371 | Good product performance but under-marketed |
| **Total classified** | **4,724** | — |

67.1% of all classified products are in Monitor status.
This is not a failure signal — Monitor simply means insufficient
consistent performance to justify active investment decisions yet.

---

## Dashboard Page 2 — What It Shows

Two charts:
1. Revenue Contribution by Product — % contribution bar chart (top 11 products)
2. Product Performance Matrix — scatter plot with 4 quadrants
   - X axis: Total Quantity
   - Y axis: Total Revenue
   - Reference lines: £100K revenue threshold, 50K quantity threshold
   - Quadrant labels with business action guidance

---

## Revenue Contribution by Product (from product_revenue_contribution)

| Rank | Product | Revenue | Contribution % |
|---|---|---|---|
| 1 | REGENCY CAKESTAND 3 TIER | £330,590 | 1.68% |
| 2 | WHITE HANGING HEART T-LIGHT HOLDER | £257,725 | 1.31% |
| 3 | JUMBO BAG RED RETROSPOT | £182,681 | 0.93% |
| 4 | PAPER CRAFT, LITTLE BIRDIE | £168,470 | 0.86% |
| 5 | PARTY BUNTING | £148,318 | 0.75% |
| 6 | ASSORTED COLOUR BIRD ORNAMENT | £129,324 | 0.66% |
| 7 | PAPER CHAIN KIT 50'S CHRISTMAS | £117,760 | 0.60% |
| 8 | MEDIUM CERAMIC TOP STORAGE JAR | £81,701 | 0.41% |
| 9 | CHILLI LIGHTS | £80,541 | 0.41% |
| 10 | POPCORN HOLDER | £79,520 | 0.40% |
| 11 | JUMBO BAG PINK POLKADOT | £76,325 | 0.39% |

Top 10 combined: approximately 8.35% of total revenue.
The remaining 91.65% is distributed across hundreds of other products.

---

## Product Performance Matrix — 4 Quadrants

### Quadrant 1 — Superstar Products (High Revenue + High Quantity)
Revenue above £100K AND Quantity above 50K units.
Business action: Protect inventory · Increase marketing · Avoid stockouts

Products confirmed in this quadrant:
| Product | Revenue | Quantity |
|---|---|---|
| WHITE HANGING HEART T-LIGHT HOLDER | £257,725 | 94,203 |
| JUMBO BAG RED RETROSPOT | £182,681 | 97,176 |
| PAPER CRAFT, LITTLE BIRDIE | £168,470 | 80,995 |
| ASSORTED COLOUR BIRD ORNAMENT | £129,324 | 80,082 |

### Quadrant 2 — Premium Products (High Revenue + Lower Quantity)
Revenue above £100K AND Quantity below 50K units.
Business action: Premium positioning · Cross-sell · Higher-margin promotions

Products confirmed in this quadrant:
| Product | Revenue | Quantity |
|---|---|---|
| REGENCY CAKESTAND 3 TIER | £330,590 | 26,478 |
| PARTY BUNTING | £148,318 | 28,200 |
| PAPER CHAIN KIT 50'S CHRISTMAS | £117,760 | 35,084 |

### Quadrant 3 — Mass Market Products (Lower Revenue + High Quantity)
Revenue below £100K AND Quantity above 50K units.
Business action: Volume efficiency review · Minimum order quantity thresholds

Products confirmed in this quadrant:
| Product | Revenue | Quantity |
|---|---|---|
| WORLD WAR 2 GLIDERS ASSTD DESIGNS | £24,446 | 106,139 |
| BROCADE RING PURSE | £14,766 | 70,369 |
| PACK OF 60 PINK PAISLEY CAKE CASES | £28,082 | 56,061 |

### Quadrant 4 — Underperforming Products (Low Revenue + Low Quantity)
Revenue below £100K AND Quantity below 50K units.
This quadrant contains the majority of the product catalog.
Business action: Monitor quarterly. Review for discontinuation if
two consecutive quarters show declining or flat performance.

Notable products in this quadrant from the scatter plot:
£80,541 (CHILLI LIGHTS) · £79,520 (POPCORN HOLDER) ·
£76,325 (JUMBO BAG PINK POLKADOT) · £71,106 (LUNCH BAG RED RETROSPOT) ·
£69,002 (JUMBO BAG STRAWBERRY) · £65,189 (BLACK RECORD COVER FRAME)

---

## What This Data Found — Key Business Findings

### Finding 1 — No Single Product Dominates Revenue
The top product (REGENCY CAKESTAND, £330,590) contributes only 1.68%
of total revenue. The top 10 combined contribute approximately 8.35%.
This means 91.65% of revenue comes from hundreds of other products.
Revenue is highly diversified — this is both a strength (reduces
single-product risk) and a complexity challenge (portfolio management
across thousands of SKUs is operationally demanding).

### Finding 2 — Paper Craft Little Birdie Is a Bulk Purchase Anomaly
£168,470 from exactly 1 order. This is not a product with organic
recurring demand. It is a single wholesale bulk purchase event.
It appears in 4th position on the revenue chart and creates a false
impression of being a strong product line.
Any demand forecasting or inventory planning that treats this product
as having normal demand patterns will be seriously wrong.
This product should be excluded from any trend analysis or forecast
and flagged explicitly in all product reports.

### Finding 3 — Revenue Leaders and Volume Leaders Are Different Products
The highest-revenue product (CAKESTAND, £330,590) has only 26,478 units.
The highest-volume product (WW2 GLIDERS, 106,139 units) has £24,446 revenue.
These are fundamentally different product economics.
Business planning using only revenue rankings misses high-volume
low-margin products. Planning using only quantity rankings misses
high-value low-volume products.
The performance matrix is the correct tool for a complete picture.

### Finding 4 — WHITE HANGING HEART T-LIGHT HOLDER Is the True Star Product
This product is the only one that appears in:
- Top 3 by revenue (£257,725, rank 2)
- Top 4 by quantity (94,203 units, rank 4)
- Top 3 by order count (5,365 orders, rank 2)
- Superstar quadrant in the performance matrix

It is the most consistent multi-dimensional performer in the catalog.
It represents the ideal product profile for this business type.
Any stockout on this product represents a direct, measurable
revenue loss across a large number of customers.

### Finding 5 — Cakestand Has Premium Product Economics
£330,590 from 26,478 units = £12.49 average revenue per unit.
£257,725 from 94,203 units = £2.73 average revenue per unit (Heart T-Light).
The Cakestand generates 4.6x more revenue per unit despite selling
3.6x fewer units. This is classic Premium product behavior — high
unit price, lower volume, high total revenue.
This product should be treated as a premium line with potential for
cross-sell and upsell, not as a volume product.

### Finding 6 — Medium Ceramic Storage Jar Shows Wholesale Bulk Ordering
£81,701 from only 247 orders = £331 average order value.
78,033 units across 247 orders = approximately 316 units per order.
This pattern indicates B2B wholesale bulk purchasing behavior.
A customer ordering 316 units at a time is a trade buyer, not a retail
buyer. This product may need separate treatment in the customer model
— bulk buyers of this product are likely in the Champions or Loyal
segment but with very different ordering patterns to typical customers.

### Finding 7 — 3,172 Products on Monitor Is Normal for This Catalog
67% of classified products in Monitor status sounds concerning but is
correct for a wholesale gifting catalog of this size and diversity.
Most SKUs at any point in time are either:
- seasonal (only active 3-4 months per year)
- niche (serve a specific customer subset)
- declining (being phased out)

The Monitor classification preserves visibility without committing
resources. The 810 Invest More and 371 Premium Focus products are
the active investment portfolio.

---

## Where These Findings Were Pasted

These findings were added to:

1. `knowledge_base/project_findings/product_intelligence_findings.md`
   → This file (complete findings)

2. `docs/data_findings.md`
   → New Section: Product Findings added with top product tables

3. `tableau/README.md`
   → Dashboard 6 and 7 sections: Product Intelligence P1 and P2
   → Key numbers, chart descriptions, business insight, and anomaly note

4. `README.md` (root)
   → Product Intelligence section added to Key Results
   → Top 5 by revenue and quantity tables
   → Investment strategy distribution table
   → Product performance quadrant table

---

## SQL Views Summary

All five views connect to the Product Intelligence dashboard:

```sql
-- product_revenue_analysis
-- Aggregates revenue and quantity per description
-- Ordered by total_revenue DESC
-- All rows filtered to is_merchandise = TRUE

-- product_quantity_analysis
-- Same aggregation but ordered by total_quantity DESC

-- product_revenue_contribution
-- Adds revenue_contribution_pct = total_revenue / SUM(total_revenue) * 100

-- product_performance_matrix
-- Combines revenue, quantity, and order count per product
-- Used to plot the 4-quadrant scatter chart in Tableau

-- product_investment_analysis
-- Classifies each product into one of 4 investment strategies
-- Based on revenue thresholds and order count thresholds
-- investment_strategy values: Monitor, Invest More, Premium Focus,
--   Marketing Opportunity
```

All views use fact_sales joined to dim_product with is_merchandise = TRUE filter.
Revenue totals in product views reconcile to merchandise revenue benchmark
of £19,701,497.66 (not total revenue which includes postage and adjustments).

---

## Important Warning for Dashboard Users

**Paper Craft Little Birdie must be handled carefully in all reports.**

When this product appears in any top-10 list, add a footnote:
"PAPER CRAFT, LITTLE BIRDIE (£168,470) represents a single bulk
purchase order and is not a recurring demand product. It should
be excluded from trend analysis and demand forecasting."

If it is not flagged, any business stakeholder looking at the
product revenue chart will incorrectly assume it is a strong
ongoing product line and may make inventory or investment decisions
based on a one-time event.
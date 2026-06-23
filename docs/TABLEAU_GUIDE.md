# Tableau Dashboard — User Guide

## How to Open

1. Install **Tableau Public** (free) from tableau.com/products/public
2. Open `tableau/retail_dashboard.twbx`
3. If prompted for a data source, point it to your PostgreSQL database (see README for credentials)

## Dashboard Pages

### Page 1 — Executive Summary
KPI scorecards: Total Revenue, Gross Margin %, Orders, Unique Customers.
Use the **date range filter** (top right) to change the period.

### Page 2 — Revenue Trends
Year-over-year revenue chart. Green = above prior year. Red = below.
Click any bar to drill down by store or category.

### Page 3 — Anomaly Alerts
Days flagged by the ML model as unusual. Red dots = anomaly detected.
Hover over any dot to see the store, date, and revenue deviation.

### Page 4 — Customer RFM Segments
Scatter plot of customer segments. The **"At Risk — High Value"** bubble
represents customers worth targeting for re-engagement.

## Filters Available
- Date range
- Store / Region
- Product Category
- Customer Segment

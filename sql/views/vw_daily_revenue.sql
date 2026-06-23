-- ============================================================
-- RETAIL REVENUE INTELLIGENCE — DAILY REVENUE VIEW
-- Version: 1.0
-- Purpose: Tableau-ready daily revenue view
-- ============================================================

\c retail_db;

DROP MATERIALIZED VIEW IF EXISTS vw_daily_revenue;

CREATE MATERIALIZED VIEW vw_daily_revenue AS
SELECT
    fs.order_date,
    dc.country_name,
    ROUND(SUM(fs.revenue), 2) AS daily_revenue,
    SUM(fs.quantity) AS daily_quantity,
    COUNT(DISTINCT fs.invoice) AS daily_orders,
    COUNT(DISTINCT CASE WHEN fs.customer_key <> 0 THEN fs.customer_key END) AS unique_customers,
    COUNT(DISTINCT fs.product_key) AS unique_products
FROM fact_sales fs
JOIN dim_country dc
    ON fs.country_key = dc.country_key
GROUP BY fs.order_date, dc.country_name
WITH DATA;

CREATE UNIQUE INDEX idx_vw_daily_revenue
ON vw_daily_revenue (order_date, country_name);
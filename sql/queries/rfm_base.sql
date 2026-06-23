-- ============================================================
-- RETAIL REVENUE INTELLIGENCE — RFM BASE QUERY
-- Version: 1.0
-- Purpose: Base customer aggregation for RFM segmentation
-- ============================================================

\c retail_db;

WITH customer_base AS (
    SELECT
        dc.customer_id,
        MAX(fs.order_date) AS last_order_date,
        COUNT(DISTINCT fs.invoice) AS frequency,
        ROUND(SUM(fs.revenue), 2) AS monetary
    FROM fact_sales fs
    JOIN dim_customer dc
        ON fs.customer_key = dc.customer_key
    WHERE fs.customer_key <> 0
    GROUP BY dc.customer_id
)
SELECT
    customer_id,
    (SELECT MAX(order_date) FROM fact_sales) - last_order_date AS recency,
    frequency,
    monetary
FROM customer_base
ORDER BY monetary DESC;
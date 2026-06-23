-- ============================================================
-- RETAIL REVENUE INTELLIGENCE — ABC PRODUCT ANALYSIS
-- Version: 1.0
-- Purpose: Product revenue contribution classification
-- ============================================================

\c retail_db;

WITH product_revenue AS (
    SELECT
        dp.product_key,
        dp.stockcode,
        dp.description,
        dp.is_merchandise,
        dp.product_type,
        ROUND(SUM(fs.revenue), 2) AS total_revenue
    FROM fact_sales fs
    JOIN dim_product dp
        ON fs.product_key = dp.product_key
    GROUP BY
        dp.product_key,
        dp.stockcode,
        dp.description,
        dp.is_merchandise,
        dp.product_type
),
ranked AS (
    SELECT
        *,
        SUM(total_revenue) OVER () AS grand_total,
        SUM(total_revenue) OVER (
            ORDER BY total_revenue DESC, product_key
        ) AS cumulative_revenue
    FROM product_revenue
)
SELECT
    stockcode,
    description,
    is_merchandise,
    product_type,
    total_revenue,
    ROUND(cumulative_revenue / grand_total * 100, 2) AS cumulative_pct,
    CASE
        WHEN cumulative_revenue / grand_total <= 0.70 THEN 'A - Core'
        WHEN cumulative_revenue / grand_total <= 0.90 THEN 'B - Secondary'
        ELSE 'C - Long Tail'
    END AS abc_class
FROM ranked
ORDER BY total_revenue DESC, stockcode;
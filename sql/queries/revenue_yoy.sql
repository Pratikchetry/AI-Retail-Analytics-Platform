-- ============================================================
-- RETAIL REVENUE INTELLIGENCE — MONTHLY REVENUE / YOY VIEW
-- Version: 1.0
-- Purpose: Monthly revenue trend with prior-year comparison
-- ============================================================

\c retail_db;

WITH monthly_revenue AS (
    SELECT
        dd.year,
        dd.month,
        dd.month_name,
        ROUND(SUM(fs.revenue), 2) AS revenue_current
    FROM fact_sales fs
    JOIN dim_date dd
        ON fs.order_date = dd.date_key
    GROUP BY dd.year, dd.month, dd.month_name
)
SELECT
    year,
    month,
    month_name,
    revenue_current,
    LAG(revenue_current, 12) OVER (ORDER BY year, month) AS revenue_prior_year,
    ROUND(
        (
            revenue_current - LAG(revenue_current, 12) OVER (ORDER BY year, month)
        ) / NULLIF(LAG(revenue_current, 12) OVER (ORDER BY year, month), 0) * 100
    , 2) AS yoy_pct_change
FROM monthly_revenue
ORDER BY year, month;
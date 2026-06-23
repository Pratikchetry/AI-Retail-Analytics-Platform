-- ============================================================
-- RETAIL REVENUE INTELLIGENCE — POST-LOAD VALIDATION
-- Validate PostgreSQL tables against notebook benchmarks
-- ============================================================

\c retail_db;

-- 1. Table row counts
SELECT 'fact_sales' AS table_name, COUNT(*) AS row_count FROM fact_sales
UNION ALL
SELECT 'fact_returns_cancellations', COUNT(*) FROM fact_returns_cancellations
UNION ALL
SELECT 'fact_accounting_adjustments', COUNT(*) FROM fact_accounting_adjustments
UNION ALL
SELECT 'dim_product', COUNT(*) FROM dim_product
UNION ALL
SELECT 'dim_country', COUNT(*) FROM dim_country
UNION ALL
SELECT 'dim_customer', COUNT(*) FROM dim_customer
UNION ALL
SELECT 'dim_date', COUNT(*) FROM dim_date;

-- 2. Revenue total
SELECT ROUND(SUM(revenue), 2) AS total_sales_revenue
FROM fact_sales;

-- 3. Invoice count
SELECT COUNT(DISTINCT invoice) AS unique_invoices
FROM fact_sales;

-- 4. Country count
SELECT COUNT(DISTINCT country_key) AS unique_countries
FROM fact_sales;

-- 5. Stock code count through dimension
SELECT COUNT(*) AS unique_products
FROM dim_product;

-- 6. UK revenue and share
SELECT
    dc.country_name,
    ROUND(SUM(fs.revenue), 2) AS total_revenue
FROM fact_sales fs
JOIN dim_country dc
    ON fs.country_key = dc.country_key
GROUP BY dc.country_name
ORDER BY total_revenue DESC;

-- 7. Monthly revenue validation
SELECT
    dd.year,
    dd.month,
    dd.month_name,
    ROUND(SUM(fs.revenue), 2) AS monthly_revenue
FROM fact_sales fs
JOIN dim_date dd
    ON fs.order_date = dd.date_key
GROUP BY dd.year, dd.month, dd.month_name
ORDER BY dd.year, dd.month;

-- 8. Unknown customer usage
SELECT COUNT(*) AS unknown_customer_rows
FROM fact_sales
WHERE customer_key = 0;

-- 9. Customer-linked unique customers
SELECT COUNT(DISTINCT customer_key) AS customer_keys_in_fact_sales_excluding_unknown
FROM fact_sales
WHERE customer_key <> 0;

-- 10. Merchandise vs non-merchandise revenue
SELECT
    dp.is_merchandise,
    dp.product_type,
    ROUND(SUM(fs.revenue), 2) AS total_revenue
FROM fact_sales fs
JOIN dim_product dp
    ON fs.product_key = dp.product_key
GROUP BY dp.is_merchandise, dp.product_type
ORDER BY dp.is_merchandise DESC, total_revenue DESC;
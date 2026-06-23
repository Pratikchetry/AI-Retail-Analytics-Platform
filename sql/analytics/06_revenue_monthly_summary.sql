DROP TABLE IF EXISTS revenue_monthly_summary;

CREATE TABLE revenue_monthly_summary AS

SELECT

    EXTRACT(YEAR FROM order_date) AS year,
    EXTRACT(MONTH FROM order_date) AS month,

    DATE_TRUNC('month', order_date)::date AS month_date,

    TO_CHAR(order_date,'Mon') AS month_name,

    ROUND(SUM(revenue),2) AS total_revenue,
    ROUND(AVG(revenue),2) AS avg_daily_revenue,
    COUNT(DISTINCT invoice) AS total_orders

FROM fact_sales

GROUP BY
    EXTRACT(YEAR FROM order_date),
    EXTRACT(MONTH FROM order_date),
    DATE_TRUNC('month', order_date),
    TO_CHAR(order_date,'Mon')

ORDER BY year, month;
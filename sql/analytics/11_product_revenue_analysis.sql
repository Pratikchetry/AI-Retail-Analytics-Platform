DROP TABLE IF EXISTS product_revenue_analysis;

CREATE TABLE product_revenue_analysis AS

SELECT

    dp.product_key,
    dp.stockcode,
    dp.description,

    ROUND(
        SUM(fs.revenue),
        2
    ) AS total_revenue,

    SUM(fs.quantity) AS total_quantity,

    COUNT(DISTINCT fs.invoice) AS total_orders

FROM fact_sales fs

JOIN dim_product dp
ON fs.product_key = dp.product_key

WHERE
    dp.is_merchandise = TRUE
    AND dp.description IS NOT NULL

GROUP BY

    dp.product_key,
    dp.stockcode,
    dp.description

ORDER BY total_revenue DESC;
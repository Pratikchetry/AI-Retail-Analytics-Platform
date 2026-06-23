DROP TABLE IF EXISTS customer_rfm_base;

CREATE TABLE customer_rfm_base AS

WITH snapshot_date AS (
    SELECT MAX(order_date) AS max_date
    FROM fact_sales
)

SELECT
    dc.customer_key,
    dc.customer_id,

    (
        SELECT max_date
        FROM snapshot_date
    ) - MAX(fs.order_date) AS recency_days,

    COUNT(DISTINCT fs.invoice) AS frequency,

    ROUND(
        SUM(fs.revenue),
        2
    ) AS monetary_value

FROM fact_sales fs

JOIN dim_customer dc
ON fs.customer_key = dc.customer_key

WHERE dc.customer_id <> -1

GROUP BY
    dc.customer_key,
    dc.customer_id;
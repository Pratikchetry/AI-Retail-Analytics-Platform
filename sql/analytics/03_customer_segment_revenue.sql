DROP TABLE IF EXISTS customer_segment_revenue;

CREATE TABLE customer_segment_revenue AS

SELECT

    r.customer_segment,

    COUNT(DISTINCT r.customer_id) AS customer_count,

    ROUND(
        SUM(fs.revenue),
        2
    ) AS total_revenue,

    ROUND(
        AVG(fs.revenue),
        2
    ) AS avg_order_revenue

FROM customer_rfm_segmentation r

JOIN fact_sales fs
ON r.customer_key = fs.customer_key

GROUP BY
    r.customer_segment;
DROP TABLE IF EXISTS customer_segment_profile;

CREATE TABLE customer_segment_profile AS

SELECT

    customer_segment,

    ROUND(AVG(recency_days),2) AS avg_recency,

    ROUND(AVG(frequency),2) AS avg_frequency,

    ROUND(AVG(monetary_value),2) AS avg_monetary,

    COUNT(*) AS customer_count

FROM customer_rfm_segmentation

GROUP BY customer_segment;
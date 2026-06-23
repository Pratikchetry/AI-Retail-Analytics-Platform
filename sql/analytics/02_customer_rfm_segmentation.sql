DROP TABLE IF EXISTS customer_rfm_segmentation;

CREATE TABLE customer_rfm_segmentation AS

WITH rfm_scores AS (

    SELECT

        customer_key,
        customer_id,
        recency_days,
        frequency,
        monetary_value,

        NTILE(5) OVER (
            ORDER BY recency_days DESC
        ) AS r_score,

        NTILE(5) OVER (
            ORDER BY frequency ASC
        ) AS f_score,

        NTILE(5) OVER (
            ORDER BY monetary_value ASC
        ) AS m_score

    FROM customer_rfm_base

),

rfm_final AS (

    SELECT
        *,
        (r_score + f_score + m_score) AS total_rfm_score

    FROM rfm_scores

)

SELECT

    customer_key,
    customer_id,
    recency_days,
    frequency,
    monetary_value,

    r_score,
    f_score,
    m_score,

    total_rfm_score,

    CASE

        WHEN total_rfm_score >= 13
        THEN 'Champions'

        WHEN total_rfm_score BETWEEN 10 AND 12
        THEN 'Loyal Customers'

        WHEN total_rfm_score BETWEEN 8 AND 9
        THEN 'Potential Loyalists'

        WHEN total_rfm_score BETWEEN 5 AND 7
        THEN 'At Risk'

        ELSE 'Lost Customers'

    END AS customer_segment

FROM rfm_final;
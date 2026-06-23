DROP TABLE IF EXISTS product_investment_analysis;

CREATE TABLE product_investment_analysis AS

WITH thresholds AS (

    SELECT

        PERCENTILE_CONT(0.75)
        WITHIN GROUP (ORDER BY total_revenue) AS revenue_threshold,

        PERCENTILE_CONT(0.75)
        WITHIN GROUP (ORDER BY total_quantity) AS quantity_threshold

    FROM product_performance_matrix

)

SELECT

    ppm.description,
    ppm.total_revenue,
    ppm.total_quantity,
    ppm.total_orders,

    CASE

        WHEN ppm.total_revenue >= t.revenue_threshold
             AND ppm.total_quantity >= t.quantity_threshold
        THEN 'Invest More'

        WHEN ppm.total_revenue >= t.revenue_threshold
             AND ppm.total_quantity < t.quantity_threshold
        THEN 'Premium Focus'

        WHEN ppm.total_revenue < t.revenue_threshold
             AND ppm.total_quantity >= t.quantity_threshold
        THEN 'Marketing Opportunity'

        ELSE 'Monitor'

    END AS investment_strategy

FROM product_performance_matrix ppm
CROSS JOIN thresholds t;
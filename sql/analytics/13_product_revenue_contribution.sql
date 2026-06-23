DROP TABLE IF EXISTS product_revenue_contribution;

CREATE TABLE product_revenue_contribution AS

WITH product_sales AS (

    SELECT

        dp.description,

        ROUND(
            SUM(fs.revenue),
            2
        ) AS total_revenue

    FROM fact_sales fs

    JOIN dim_product dp
    ON fs.product_key = dp.product_key

    WHERE
        dp.is_merchandise = TRUE
        AND dp.description IS NOT NULL

    GROUP BY dp.description

),

total_company_revenue AS (

    SELECT
        SUM(total_revenue) AS company_revenue
    FROM product_sales

)

SELECT

    ps.description,

    ps.total_revenue,

    ROUND(
        (ps.total_revenue / tcr.company_revenue) * 100,
        2
    ) AS revenue_contribution_pct

FROM product_sales ps

CROSS JOIN total_company_revenue tcr

ORDER BY total_revenue DESC;
DROP TABLE IF EXISTS revenue_growth_analysis;

CREATE TABLE revenue_growth_analysis AS

WITH monthly_data AS (

    SELECT

        DATE_TRUNC(
            'month',
            TO_DATE(
                year::text || '-' || month::text || '-01',
                'YYYY-MM-DD'
            )
        )::date AS month_date,

        year,
        month,
        month_name,

        total_revenue

    FROM revenue_monthly_summary

),

growth_calc AS (

    SELECT

        month_date,

        TO_CHAR(
            month_date,
            'Mon YYYY'
        ) AS month_year,

        year,
        month,
        month_name,

        total_revenue,

        LAG(total_revenue) OVER (
            ORDER BY month_date
        ) AS previous_month_revenue

    FROM monthly_data

)

SELECT

    month_date,
    month_year,

    year,
    month,
    month_name,

    total_revenue,

    previous_month_revenue,

    ROUND(
        (
            (total_revenue - previous_month_revenue)
            /
            NULLIF(previous_month_revenue,0)
        ) * 100,
        2
    ) AS growth_percent

FROM growth_calc

ORDER BY month_date;
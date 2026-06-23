DROP TABLE IF EXISTS revenue_executive_summary;

CREATE TABLE revenue_executive_summary AS

WITH revenue_stats AS (

    SELECT

        SUM(total_revenue) AS total_revenue,

        AVG(total_revenue) AS avg_monthly_revenue,

        MAX(total_revenue) AS best_month_revenue,

        MIN(total_revenue) AS worst_month_revenue

    FROM revenue_monthly_summary

),

best_month AS (

    SELECT
        month_name || ' ' || year AS best_month

    FROM revenue_monthly_summary

    ORDER BY total_revenue DESC

    LIMIT 1

),

worst_month AS (

    SELECT
        month_name || ' ' || year AS worst_month

    FROM revenue_monthly_summary

    ORDER BY total_revenue ASC

    LIMIT 1

),

growth AS (

    SELECT

        ROUND(

            (
                SUM(CASE WHEN year = 2011 THEN total_revenue END)
                -
                SUM(CASE WHEN year = 2010 THEN total_revenue END)
            )

            /

            NULLIF(
                SUM(CASE WHEN year = 2010 THEN total_revenue END)
            ,0)

            * 100

        ,2) AS yoy_growth

    FROM revenue_monthly_summary

)

SELECT

    ROUND(total_revenue,2) AS total_revenue,
    ROUND(avg_monthly_revenue,2) AS avg_monthly_revenue,

    best_month,
    worst_month,

    ROUND(best_month_revenue,2) AS best_month_revenue,
    ROUND(worst_month_revenue,2) AS worst_month_revenue,

    yoy_growth

FROM revenue_stats,
     best_month,
     worst_month,
     growth;
DROP TABLE IF EXISTS yoy_revenue_analysis;

CREATE TABLE yoy_revenue_analysis AS

SELECT

    month,
    month_name,

    MAX(
        CASE
            WHEN year = 2010
            THEN total_revenue
        END
    ) AS revenue_2010,

    MAX(
        CASE
            WHEN year = 2011
            THEN total_revenue
        END
    ) AS revenue_2011,

    ROUND(

        (
            MAX(
                CASE
                    WHEN year = 2011
                    THEN total_revenue
                END
            )

            -

            MAX(
                CASE
                    WHEN year = 2010
                    THEN total_revenue
                END
            )

        )

        /

        NULLIF(

            MAX(
                CASE
                    WHEN year = 2010
                    THEN total_revenue
                END
            )

        ,0)

        * 100

    ,2) AS yoy_growth_percent

FROM revenue_monthly_summary

WHERE year IN (2010,2011)

GROUP BY
    month,
    month_name

ORDER BY month;
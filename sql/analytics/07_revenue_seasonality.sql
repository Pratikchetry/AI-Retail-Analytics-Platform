DROP TABLE IF EXISTS revenue_seasonality;

CREATE TABLE revenue_seasonality AS

SELECT

    year,
    month,
    month_name,
    total_revenue,
    total_orders

FROM revenue_monthly_summary

ORDER BY
    year,
    month;
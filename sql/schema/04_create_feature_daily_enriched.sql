DROP TABLE IF EXISTS feature_daily_enriched;

CREATE TABLE feature_daily_enriched AS

WITH daily_base AS (

    SELECT
        order_date,

        SUM(revenue) AS daily_revenue,

        COUNT(DISTINCT invoice) AS daily_orders,

        COUNT(DISTINCT customer_key) AS daily_active_customers,

        AVG(revenue) AS avg_transaction_value,

        MAX(revenue) AS largest_single_transaction

    FROM fact_sales

    GROUP BY order_date

),

holiday_features AS (

    SELECT
        holiday_date,
        holiday_name,
        is_public_holiday,
        is_peak_period

    FROM dim_holiday_uk

)

SELECT

    db.order_date,

    db.daily_revenue,

    db.daily_orders,

    db.daily_active_customers,

    ROUND(db.avg_transaction_value::numeric, 2)
        AS avg_transaction_value,

    ROUND(db.largest_single_transaction::numeric, 2)
        AS largest_single_transaction,

    CASE
    WHEN db.largest_single_transaction >
         (
            SELECT PERCENTILE_CONT(0.95)
            WITHIN GROUP (
                ORDER BY daily_max_transaction
            )
            FROM (
                SELECT
                    order_date,
                    MAX(revenue) AS daily_max_transaction
                FROM fact_sales
                GROUP BY order_date
            ) t
         )
    THEN 1
    ELSE 0
END AS large_order_flag,

    EXTRACT(DOW FROM db.order_date)
        AS day_of_week,

    EXTRACT(MONTH FROM db.order_date)
        AS month,

    EXTRACT(WEEK FROM db.order_date)
        AS week_of_year,

    CASE
        WHEN EXTRACT(DOW FROM db.order_date) IN (0, 6)
        THEN 1
        ELSE 0
    END AS is_weekend,

    CASE
        WHEN EXTRACT(MONTH FROM db.order_date)
             IN (10,11,12)
        THEN 1
        ELSE 0
    END AS is_peak_season,

    hf.holiday_name,

    COALESCE(hf.is_public_holiday, FALSE)
        AS is_public_holiday,

    COALESCE(hf.is_peak_period, FALSE)
        AS holiday_peak_period

FROM daily_base db

LEFT JOIN holiday_features hf
    ON db.order_date = hf.holiday_date

ORDER BY db.order_date;
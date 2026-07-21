DROP TABLE IF EXISTS feature_daily_model_input CASCADE;

CREATE TABLE feature_daily_model_input AS

SELECT

    order_date,

    daily_revenue,

    daily_orders,

    daily_active_customers,

    avg_transaction_value,

    largest_single_transaction,

    large_order_flag,

    day_of_week,

    month,

    week_of_year,

    is_weekend,

    is_peak_season,

    is_public_holiday,

    holiday_peak_period,

    -- Revenue lag features

    LAG(daily_revenue, 1)
        OVER (ORDER BY order_date)
        AS revenue_lag_1,

    LAG(daily_revenue, 7)
        OVER (ORDER BY order_date)
        AS revenue_lag_7,

    LAG(daily_revenue, 14)
        OVER (ORDER BY order_date)
        AS revenue_lag_14,

    LAG(daily_revenue, 28)
        OVER (ORDER BY order_date)
        AS revenue_lag_28,

    -- Order lag features

    LAG(daily_orders, 1)
        OVER (ORDER BY order_date)
        AS orders_lag_1,

    LAG(daily_orders, 7)
        OVER (ORDER BY order_date)
        AS orders_lag_7,

    -- Rolling revenue means

    ROUND(
        AVG(daily_revenue)
        OVER (
            ORDER BY order_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        )::numeric,
        2
    ) AS rolling_mean_7,

    ROUND(
        AVG(daily_revenue)
        OVER (
            ORDER BY order_date
            ROWS BETWEEN 13 PRECEDING AND CURRENT ROW
        )::numeric,
        2
    ) AS rolling_mean_14,

    -- Rolling volatility

    ROUND(
        STDDEV(daily_revenue)
        OVER (
            ORDER BY order_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        )::numeric,
        2
    ) AS rolling_std_7,

    ROUND(
        STDDEV(daily_revenue)
        OVER (
            ORDER BY order_date
            ROWS BETWEEN 13 PRECEDING AND CURRENT ROW
        )::numeric,
        2
    ) AS rolling_std_14,

    -- Revenue growth

    ROUND(
        (
            daily_revenue
            -
            LAG(daily_revenue, 7)
            OVER (ORDER BY order_date)
        )
        /
        NULLIF(
            LAG(daily_revenue, 7)
            OVER (ORDER BY order_date),
            0
        ),
        4
    ) AS revenue_growth_7d,

    -- Orders growth

    ROUND(
        (
            daily_orders
            -
            LAG(daily_orders, 7)
            OVER (ORDER BY order_date)
        )::numeric
        /
        NULLIF(
            LAG(daily_orders, 7)
            OVER (ORDER BY order_date),
            0
        ),
        4
    ) AS orders_growth_7d

FROM feature_daily_enriched

ORDER BY order_date;
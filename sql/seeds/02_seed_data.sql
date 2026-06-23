-- ============================================================
-- RETAIL REVENUE INTELLIGENCE — SEED DATA
-- Populate dim_date based on Online Retail II project timeline
-- Run this after schema creation
-- ============================================================

\c retail_db;

INSERT INTO dim_date (
    date_key,
    year,
    quarter,
    month,
    month_name,
    week,
    day_of_week,
    day_name,
    is_weekend
)
SELECT
    d::DATE AS date_key,
    EXTRACT(YEAR FROM d)::INT AS year,
    EXTRACT(QUARTER FROM d)::INT AS quarter,
    EXTRACT(MONTH FROM d)::INT AS month,
    TRIM(TO_CHAR(d, 'Month'))::VARCHAR(20) AS month_name,
    EXTRACT(WEEK FROM d)::INT AS week,
    EXTRACT(DOW FROM d)::INT AS day_of_week,
    TRIM(TO_CHAR(d, 'Day'))::VARCHAR(15) AS day_name,
    CASE
        WHEN EXTRACT(DOW FROM d) IN (0, 6) THEN TRUE
        ELSE FALSE
    END AS is_weekend
FROM generate_series(
    '2009-12-01'::DATE,
    '2011-12-31'::DATE,
    '1 day'::INTERVAL
) AS d
ON CONFLICT (date_key) DO NOTHING;
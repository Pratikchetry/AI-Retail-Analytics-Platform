DROP TABLE IF EXISTS dim_holiday_uk;

CREATE TABLE dim_holiday_uk (
    holiday_date DATE PRIMARY KEY,
    holiday_name VARCHAR(100),
    is_public_holiday BOOLEAN,
    holiday_type VARCHAR(50),
    is_peak_period BOOLEAN
);
DROP VIEW IF EXISTS vw_ml_training_data;

CREATE VIEW vw_ml_training_data AS

SELECT *

FROM feature_daily_model_input

WHERE
    revenue_lag_28 IS NOT NULL
    AND revenue_growth_7d IS NOT NULL
    AND orders_growth_7d IS NOT NULL

ORDER BY order_date;
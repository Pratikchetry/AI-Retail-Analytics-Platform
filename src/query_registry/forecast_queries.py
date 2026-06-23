"""
Phase 2 — AI Retail Intelligence Platform
Canonical SQL Query Registry for Machine Learning Revenue Forecasts and Statistical Error Tracking.
"""

FORECAST_QUERIES = {
    "future_revenue_projections": """
        -- Purpose: Extracts the forward-looking projected revenue metrics for downstream planning
        SELECT 
            ds,
            yhat AS projected_revenue,
            yhat_lower AS pessimistic_bound,
            yhat_upper AS optimistic_bound
        FROM revenue_forecast
        WHERE ds >= CURRENT_DATE
        ORDER BY ds ASC;
    """,

    "forecast_model_accuracy": """
        -- Purpose: Exposes backtest residuals and evaluation errors to evaluate pipeline reliability
        SELECT 
            evaluation_date,
            model_version,
            mae AS mean_absolute_error,
            rmse AS root_mean_squared_error,
            mape AS mean_absolute_percentage_error
        FROM forecast_error_metrics
        ORDER BY evaluation_date DESC
        LIMIT 1;
    """,

    "projected_growth_milestones": """
        -- Purpose: Summarizes upcoming forecast thresholds to locate peak high-demand windows
        SELECT 
            STRFTIME('%Y-%m', ds) AS forecast_month,
            SUM(yhat) AS expected_monthly_total,
            MAX(yhat) AS projected_peak_daily_surge
        FROM revenue_forecast
        WHERE ds >= CURRENT_DATE
        GROUP BY forecast_month
        ORDER BY forecast_month ASC;
    """
}
"""
Phase 2 — AI Retail Intelligence Platform
Semantic Metadata Mapping for Machine Learning Forward Projections and Target Residuals.
"""

FORECAST_METADATA = {
    "tables": {
        "revenue_forecast": {
            "description": "Forward-looking multi-horizon revenue forecasts generated via automated pipeline routines.",
            "columns": {
                "ds": "The explicitly scheduled target date of the projected trend (YYYY-MM-DD).",
                "yhat": "The localized expected mean projection calculation value for top-line revenue.",
                "yhat_lower": "The conservative, pessimistic boundary layer of the revenue confidence interval.",
                "yhat_upper": "The aggressive, optimistic boundary layer of the revenue confidence interval."
            }
        },
        "forecast_error_metrics": {
            "description": "Residual valuation data representing systemic pipeline model errors.",
            "columns": {
                "evaluation_date": "The calendar marker when backtesting accuracy measurements were computed.",
                "model_version": "The semantic registration label tracking the model variation build version.",
                "mae": "Mean Absolute Error metric tracking pure currency dollar deviation variances.",
                "rmse": "Root Mean Squared Error metric focusing penalization heavily on wider outlier mistakes.",
                "mape": "Mean Absolute Percentage Error conveying deviation performance as relative scales."
            }
        }
    }
}
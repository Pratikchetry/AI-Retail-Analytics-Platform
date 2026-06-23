"""
Phase 2 — AI Retail Intelligence Platform
Semantic Metadata Mapping for ML Anomaly Scores, Volatility, and Outliers.
"""

ANOMALY_METADATA = {
    "table_name": "ml_anomaly_scores",
    "description": "Contains statistical anomalies and deviations calculated via isolation forests on daily retail revenue tracking.",
    "columns": {
        "date": "The explicit calendar date of the tracking window (YYYY-MM-DD).",
        "country_name": "The geographic market location associated with the revenue generation.",
        "daily_revenue": "The absolute actual gross financial yield captured for that day.",
        "expected_baseline": "The mathematically calculated expected revenue figure based on historical trends.",
        "anomaly_score": "Continuous numerical value representing the severity of deviation. Higher means more volatile.",
        "is_anomaly": "Boolean flag (TRUE/FALSE) identifying whether the transaction behavior crossed standard thresholds.",
        "anomaly_direction": "Categorical flag indicating the movement type: 'spike' (unusual boom) or 'drop' (unusual decay)."
    },
    "business_context": "Use this layout whenever the user asks about out-of-bounds events, data spikes, drops, market disruptions, or operational volatility."
}
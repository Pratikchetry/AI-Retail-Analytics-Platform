"""
Phase 2 — AI Retail Intelligence Platform
Canonical SQL Query Registry for ML Anomaly Scores, Outliers, and Operational Drift.
These queries serve as complex few-shot training tokens for the agentic parser.
"""

ANOMALY_QUERIES = {
    "all_active_anomalies": """
        -- Purpose: Extracts all verified mathematical anomalies across the retail footprint
        SELECT 
            date,
            country_name,
            daily_revenue,
            expected_baseline,
            anomaly_score,
            anomaly_direction
        FROM ml_anomaly_scores
        WHERE is_anomaly = TRUE
        ORDER BY anomaly_score DESC, date DESC;
    """,

    "regional_drift_summary": """
        -- Purpose: Evaluates which regional markets are exhibiting the highest rate of volatile deviations
        SELECT 
            country_name,
            COUNT(*) AS total_data_points,
            SUM(CASE WHEN is_anomaly = TRUE THEN 1 ELSE 0 END) AS anomaly_count,
            (SUM(CASE WHEN is_anomaly = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS anomaly_rate_pct,
            AVG(anomaly_score) AS mean_volatility_score
        FROM ml_anomaly_scores
        GROUP BY country_name
        ORDER BY anomaly_count DESC, anomaly_rate_pct DESC;
    """,

    "high_magnitude_revenue_drops": """
        -- Purpose: Pinpoints systemic revenue collapses/drops that break historical baseline expectations
        SELECT 
            date,
            country_name,
            daily_revenue,
            expected_baseline,
            (expected_baseline - daily_revenue) AS revenue_deficit,
            anomaly_score
        FROM ml_anomaly_scores
        WHERE is_anomaly = TRUE 
          AND anomaly_direction = 'drop'
        ORDER BY revenue_deficit DESC;
    """,

    "unexplained_revenue_spikes": """
        -- Purpose: Highlights explosive market growth events or technical data-logging anomalies
        SELECT 
            date,
            country_name,
            daily_revenue,
            expected_baseline,
            (daily_revenue - expected_baseline) AS revenue_surplus,
            anomaly_score
        FROM ml_anomaly_scores
        WHERE is_anomaly = TRUE 
          AND anomaly_direction = 'spike'
        ORDER BY revenue_surplus DESC;
    """,

    "recent_systemic_drift": """
        -- Purpose: Monitors the last 14 days for ongoing, consecutive operational out-of-bounds metrics
        SELECT 
            date,
            COUNT(CASE WHEN is_anomaly = TRUE THEN 1 END) AS active_anomalies_count,
            AVG(anomaly_score) AS average_daily_volatility,
            SUM(daily_revenue) AS cumulative_monitored_revenue
        FROM ml_anomaly_scores
        GROUP BY date
        ORDER BY date DESC
        LIMIT 14;
    """
}
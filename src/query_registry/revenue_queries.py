"""
Phase 2 — AI Retail Intelligence Platform
Canonical SQL Query Registry for Financial Closures, Seasonality, and Growth Vectors.
"""

REVENUE_QUERIES = {
    "historical_time_series": """
        -- Purpose: Builds an end-to-end operational trend view across the entire data tracking history
        SELECT 
            year,
            month,
            month_name,
            total_revenue,
            total_orders
        FROM revenue_monthly_summary
        ORDER BY year ASC, month ASC;
    """,

    "yoy_macro_variance": """
        -- Purpose: Compares monthly revenue against previous cycles to evaluate clean historical scale
        SELECT 
            month_name,
            revenue_2010,
            revenue_2011,
            yoy_growth_percent
        FROM yoy_revenue_analysis
        ORDER BY month ASC;
    """,

    "seasonal_demand_profiles": """
        -- Purpose: Pinpoints recurring seasonal performance shifts by tracking average indices over time
        SELECT 
            month_name,
            avg_revenue_contribution,
            seasonality_index
        FROM revenue_seasonality
        ORDER BY seasonality_index DESC;
    """
}
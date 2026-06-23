"""
Phase 2 — AI Retail Intelligence Platform
Canonical SQL Query Registry for Executive Performance & Cross-Domain KPIs.
"""

EXECUTIVE_QUERIES = {
    "ceo_macro_health": """
        -- Purpose: Multi-table corporate snapshot combining global metrics, top segments, and top channels
        SELECT 
            es.total_revenue,
            es.avg_monthly_revenue,
            es.best_month,
            es.best_month_revenue,
            csr.customer_segment AS dominant_segment,
            csr.total_revenue AS segment_revenue,
            (csr.total_revenue / es.total_revenue) * 100.0 AS segment_contribution_pct
        FROM revenue_executive_summary es
        CROSS JOIN customer_segment_revenue csr
        WHERE csr.total_revenue = (SELECT MAX(total_revenue) FROM customer_segment_revenue);
    """,

    "business_velocity_index": """
        -- Purpose: Evaluates current transactional momentum by balancing MoM metrics with YoY metrics
        SELECT 
            rms.year,
            rms.month,
            rms.month_name,
            rms.total_revenue,
            rga.growth_percent AS mom_growth,
            yra.yoy_growth_percent AS yoy_growth
        FROM revenue_monthly_summary rms
        LEFT JOIN revenue_growth_analysis rga ON rms.year = rga.year AND rms.month = rga.month
        LEFT JOIN yoy_revenue_analysis yra ON rms.month = yra.month
        ORDER BY rms.year DESC, rms.month DESC
        LIMIT 6;
    """,

    "operational_drag_assessment": """
        -- Purpose: Isolates lagging market segments that show worrying high-recency drift values
        SELECT 
            customer_segment,
            customer_count,
            avg_recency AS days_inactive,
            avg_frequency AS buying_frequency
        FROM customer_segment_profile
        WHERE avg_recency > (SELECT AVG(avg_recency) FROM customer_segment_profile)
        ORDER BY avg_recency DESC;
    """
}
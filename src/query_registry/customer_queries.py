"""
Phase 2 — AI Retail Intelligence Platform
Canonical SQL Query Registry for Customer RFM Segmentation and Strategic Retention Actions.
"""

CUSTOMER_QUERIES = {
    "rfm_distribution": """
        -- Purpose: Quantifies user base concentration and value across different performance buckets
        SELECT 
            customer_segment,
            customer_count,
            total_revenue,
            avg_order_revenue
        FROM customer_segment_revenue
        ORDER BY total_revenue DESC;
    """,

    "high_risk_dormant_cohorts": """
        -- Purpose: Flags high-value groups that show alarming signals of inactivity
        SELECT 
            customer_segment,
            customer_count,
            avg_recency AS days_since_last_purchase,
            avg_frequency AS total_historical_orders
        FROM customer_segment_profile
        WHERE avg_recency > 90 AND avg_frequency > 5
        ORDER BY avg_recency DESC;
    """,

    "retention_playbook_mapping": """
        -- Purpose: Maps operational profile groups directly to their recommended business adjustments
        SELECT 
            p.customer_segment,
            p.customer_count,
            p.avg_monetary AS segment_clv_proxy,
            r.recommended_action
        FROM customer_segment_profile p
        JOIN customer_retention_actions r ON p.customer_segment = r.customer_segment
        ORDER BY p.avg_monetary DESC;
    """,

    "segment_efficiency_metrics": """
        -- Purpose: Ranks customer categories based on the average revenue density generated per user
        SELECT 
            customer_segment,
            customer_count,
            total_revenue,
            (total_revenue / NULLIF(customer_count, 0)) AS revenue_per_capita
        FROM customer_segment_revenue
        ORDER BY revenue_per_capita DESC;
    """
}
"""
Phase 2 — AI Retail Intelligence Platform
Semantic Metadata Mapping for Revenue Calendars, Closures, and Seasonality Indices.
"""

REVENUE_METADATA = {
    "tables": {
        "revenue_monthly_summary": {
            "description": "Historical transactional milestones summarized strictly by discrete calendar increments.",
            "columns": {
                "year": "The four-digit calendar numerical tracking year container.",
                "month": "The standard numerical sequence positioning index (1 through 12).",
                "month_name": "The literal textbook label naming container (e.g., 'January').",
                "total_revenue": "Gross summarized financial cash inflows for the month container.",
                "total_orders": "The complete volume count of unique successful invoice receipts recorded."
            }
        },
        "revenue_growth_analysis": {
            "description": "Month-over-month (MoM) rolling trend tracking matrices.",
            "columns": {
                "year": "Tracking calendar marker component.",
                "month": "Tracking timeline alignment position.",
                "growth_percent": "The direct sequential trajectory variance change rate relative to the prior trailing block."
            }
        },
        "revenue_seasonality": {
            "description": "Long-term seasonal profiling data isolating macro annual weather or cyclical shopping behaviors.",
            "columns": {
                "month_name": "The targeting baseline tracking month context.",
                "avg_revenue_contribution": "The expected historic mean weight this month exerts over typical fiscal cycles.",
                "seasonality_index": "Normalized value centering around 1.0; metrics above 1.0 denote high demand surge seasons."
            }
        }
    }
}
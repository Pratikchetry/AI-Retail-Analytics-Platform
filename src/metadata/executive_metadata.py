"""
Phase 2 — AI Retail Intelligence Platform
Semantic Metadata Mapping for Corporate Macro-Health Summaries and Cross-Domain Metrics.
"""

EXECUTIVE_METADATA = {
    "table_name": "revenue_executive_summary",
    "description": "High-level generalized look at top-tier corporate performance indicators across time bounds.",
    "columns": {
        "total_revenue": "The entire captured historical gross revenue across all operational lifetimes.",
        "avg_monthly_revenue": "The mean financial intake calculated across active tracking months.",
        "best_month": "The exact date string representing the highest performing single month footprint.",
        "best_month_revenue": "The absolute maximum historical top-line value achieved during the best performing month.",
        "yoy_growth": "The annualized corporate expansion coefficient represented as an overarching percentage scale."
    },
    "associated_views": [
        "customer_segment_revenue",
        "product_performance_matrix"
    ],
    "business_context": "Deploy this schema metadata configuration when corporate leadership queries core milestones, long-range health profiles, or multi-domain high-level indicators."
}
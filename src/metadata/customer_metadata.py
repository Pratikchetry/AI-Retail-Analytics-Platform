"""
Phase 2 — AI Retail Intelligence Platform
Semantic Metadata Mapping for Customer Profiles, RFM Segments, and Retention Playbooks.
"""

CUSTOMER_METADATA = {
    "tables": {
        "customer_segment_revenue": {
            "description": "Aggregated business metrics mapped across core customer groups.",
            "columns": {
                "customer_segment": "The RFM designation category (e.g., 'Champions', 'At Risk', 'Hibernating').",
                "customer_count": "Total quantity of unique human customer assets allocated to this bucket.",
                "total_revenue": "Cumulative monetary value drawn from this user group.",
                "avg_order_revenue": "The mean financial scale generated per transaction within this cohort."
            }
        },
        "customer_segment_profile": {
            "description": "Granular statistical tracking behavior variables mapping recency, frequency, and monetary scales.",
            "columns": {
                "customer_segment": "The primary RFM cohort name.",
                "customer_count": "Total headcount inside the group.",
                "avg_recency": "The average number of elapsed days since the customer last completed a transaction.",
                "avg_frequency": "The mean volume of lifetime orders processed by this specific group.",
                "avg_monetary": "The mean financial lifetime value proxy calculated for this segment."
            }
        },
        "customer_retention_actions": {
            "description": "Corporate operational playbooks assigned to offset churn vectors.",
            "columns": {
                "customer_segment": "The target RFM audience.",
                "recommended_action": "Specific business strategy to apply (e.g., 'VIP Perks', 'Winback Campaigns', 'Ignore Drag')."
            }
        }
    }
}
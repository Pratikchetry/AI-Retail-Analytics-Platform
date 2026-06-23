"""
Phase 2 — AI Retail Intelligence Platform
Semantic Metadata Mapping for Product Matrices, Long-tail Lines, and Optimization Mixes.
"""

PRODUCT_METADATA = {
    "tables": {
        "product_revenue_contribution": {
            "description": "Pareto distribution tracking details analyzing item-level revenue contributions.",
            "columns": {
                "description": "The explicit text designation name of the product line asset.",
                "total_revenue": "Gross currency metrics pulled in via historical transactions for this line.",
                "revenue_contribution_pct": "The distinct, individual percentage share this item contributes to overall income."
            }
        },
        "product_investment_analysis": {
            "description": "Strategic portfolio optimization framework categorizing individual line items into action vectors.",
            "columns": {
                "stock_code": "Unique alphanumeric system product identifier.",
                "description": "The consumer-facing clear item title.",
                "total_revenue": "Total accumulated financial income generated.",
                "total_quantity": "The raw volumetric scale of stock items successfully processed through checkouts.",
                "investment_strategy": "The operational direction tier assigned to this product (e.g., 'Premium Focus', 'Core Driver', 'Liquidate/Exit')."
            }
        }
    }
}
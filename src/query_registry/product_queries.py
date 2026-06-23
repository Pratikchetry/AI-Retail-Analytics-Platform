"""
Phase 2 — AI Retail Intelligence Platform
Canonical SQL Query Registry for Product Mix Optimization and Contribution Matrices.
"""

PRODUCT_QUERIES = {
    "pareto_revenue_drivers": """
        -- Purpose: Maps out the core inventory lines generating the top 80% of business value
        SELECT 
            description,
            total_revenue,
            revenue_contribution_pct,
            SUM(revenue_contribution_pct) OVER (ORDER BY total_revenue DESC) AS cumulative_contribution_pct
        FROM product_revenue_contribution
        ORDER BY total_revenue DESC
        LIMIT 20;
    """,

    "portfolio_investment_mix": """
        -- Purpose: Groups performance data into distinct strategic categories for corporate action
        SELECT 
            investment_strategy,
            COUNT(*) AS product_count,
            SUM(total_revenue) AS strategy_revenue,
            AVG(total_quantity) AS average_units_moved
        FROM product_investment_analysis
        GROUP BY investment_strategy
        ORDER BY strategy_revenue DESC;
    """,

    "dead_stock_operational_drag": """
        -- Purpose: Flags low-performing, stagnant items that drag down working capital efficiency
        SELECT 
            stock_code,
            description,
            total_revenue,
            total_quantity_sold
        FROM product_performance_matrix
        WHERE performance_tier = 'Underperformer' OR total_quantity_sold < 10
        ORDER BY total_revenue ASC;
    """
}
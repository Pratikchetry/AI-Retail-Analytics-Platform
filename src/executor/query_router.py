"""
Phase 2 — AI Retail Intelligence Platform
Intelligent Semantic Traffic Router prioritizing performance-focused static lookups.
"""

import re
from typing import Dict, Any, Tuple
from src.executor.query_loader import QueryRegistryLoader

class QueryRouter:
    def __init__(self):
        self.loader = QueryRegistryLoader()
        # Direct intent mapping keys for immediate routing execution
        self.intent_map = {
            r"(anomaly|anomalies|outlier|outliers)": "all_active_anomalies",
            r"(regional drift|market volatility)": "regional_drift_summary",
            r"(revenue drop|performance drops)": "high_magnitude_revenue_drops",
            r"(revenue spike|growth spikes)": "unexplained_revenue_spikes",
            r"(rfm|customer segments|customer concentration)": "rfm_distribution",
            r"(dormant|at risk customers|inactive cohorts)": "high_risk_dormant_cohorts",
            r"(playbook|retention actions|marketing capital)": "retention_playbook_mapping",
            r"(ceo dashboard|macro health|corporate snapshot)": "ceo_macro_health",
            r"(business velocity|growth momentum|mom|yoy)": "business_velocity_index",
            r"(run rate|projected annual)": "revenue_run_rate",
            r"(projections|forecast|future revenue)": "future_revenue_projections",
            r"(accuracy|mae|rmse|mape|model error)": "forecast_model_accuracy",
            r"(pareto|80/20|top drivers)": "pareto_revenue_drivers",
            r"(dead stock|underperforming inventory|drag)": "dead_stock_operational_drag",
            r"(historical series|revenue trend|timeline)": "historical_time_series",
            r"(seasonality|seasonal index|demand profiles)": "seasonal_demand_profiles"
        }

    def route_intent(self, user_utterance: str) -> Tuple[str, str, Dict[str, Any]]:
        """
        Evaluates input text.
        Returns: Tuple of (Route Type ['STATIC' | 'DYNAMIC_AGENT'], Target Key/SQL text, Metadata context)
        """
        cleaned_utterance = user_utterance.strip().lower()

        # Check for matching canonical patterns first
        for pattern, query_key in self.intent_map.items():
            if re.search(pattern, cleaned_utterance):
                canonical_sql = self.loader.get_query(query_key)
                if canonical_sql:
                    return "STATIC", canonical_sql, {"matched_key": query_key, "strategy": "Bypass Agent Graph"}

        # No fast-track pattern matched. Delegate handling down to multi-agent state system.
        return "DYNAMIC_AGENT", user_utterance, {"strategy": "Trigger LangGraph Synthesizer"}
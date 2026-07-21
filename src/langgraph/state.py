"""
Phase 1 — AI Retail Intelligence Platform
LangGraph Agent State.

A single typed state object that flows through every node in the graph.
Each node reads what it needs and writes what it produces.
"""

from typing import TypedDict, Optional, List, Dict, Any


class AgentState(TypedDict, total=False):
    # --- Input ---
    question: str

    # --- Routing ---
    route: str            # SQL_LOOKUP | FORECAST | ANOMALY | METADATA | OUT_OF_SCOPE
    route_reason: str

    # --- RAG ---
    context: str          # retrieved business context

    # --- SQL chain ---
    sql: str
    sql_explanation: str
    validation_errors: List[str]
    validation_warnings: List[str]
    is_valid: bool

    # --- Execution ---
    rows: Any             # dataframe or string (NO_SQL_REQUIRED etc.)
    result_data: Any          # structured rows (list of dicts) for UI charts
    execution_status: str # SUCCESS | FAILED | SKIPPED

    # --- Reasoning ---
    answer: str
    reasoning: str
    evidence: str

    # --- Recommendation ---
    recommendation: str

    # --- Critic ---
    critic_score: float        # 0.0 - 1.0
    critic_feedback: str
    critic_passes: bool        # score >= threshold

    # --- Control ---
    attempt: int          # retry counter (resets per question)
    max_attempts: int
    error: str            # terminal error message if any
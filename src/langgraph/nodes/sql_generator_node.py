"""
Phase 1 — AI Retail Intelligence Platform
SQL Generator Node.

Wraps the existing SQLAgent to generate PostgreSQL from natural language.
Also increments the attempt counter so the graph's retry loops terminate.
"""

from src.agent.sql_agent import SQLAgent
from src.utils.logger import get_logger
from src.langgraph.state import AgentState

log = get_logger(__name__)


def sql_generator_node(state: AgentState) -> dict:
    """Generate SQL from the question. Bumps the retry counter."""
    question = state["question"]
    attempt = state.get("attempt", 0) + 1

    log.info("SQL generation for: '%s' (attempt %d)", question[:60], attempt)

    sql_agent = SQLAgent()
    result = sql_agent.generate_sql(question)

    log.info("Generated SQL: %s", result.sql[:120] if result.sql else "NO_SQL_REQUIRED")

    return {
        "sql": result.sql,
        "sql_explanation": result.explanation,
        "attempt": attempt,
    }
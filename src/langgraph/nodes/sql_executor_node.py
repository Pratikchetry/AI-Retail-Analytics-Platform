"""
Phase 1 — AI Retail Intelligence Platform
SQL Executor Node.

Wraps the existing QueryExecutionEngine to run validated SQL
against the PostgreSQL warehouse. Captures BOTH a text version
(for reasoning) and a structured list-of-dicts (for UI charts).
"""

import json

from src.executor.query_executor import QueryExecutionEngine
from src.utils.logger import get_logger
from src.langgraph.state import AgentState

log = get_logger(__name__)


def sql_executor_node(state: AgentState) -> dict:
    """Execute validated SQL against the warehouse."""
    sql = state.get("sql", "")

    log.info("Executing SQL: %s", sql[:80] if sql else "SKIPPED")

    # Special cases that skip execution
    if not sql or sql.strip() in ("NO_SQL_REQUIRED", "INFORMATION_NOT_AVAILABLE"):
        log.info("Execution skipped: %s", sql)
        return {"rows": sql, "execution_status": "SKIPPED", "result_data": None}

    try:
        executor = QueryExecutionEngine()
        result = executor.execute_query(sql)

        if result["status"] == "SUCCESS":
            df = result["data"]

            # Text version for the reasoning/critic nodes
            rows = str(df.head(10).to_dict()) if hasattr(df, "head") else str(df)

            # Structured version for the UI dashboard (clean JSON)
            result_data = None
            if hasattr(df, "head"):
                result_data = json.loads(
                    df.head(25).to_json(orient="records", date_format="iso")
                )

            n = len(df) if hasattr(df, "__len__") else "?"
            log.info("Execution success: %s rows returned", n)
            return {
                "rows": rows,
                "execution_status": "SUCCESS",
                "result_data": result_data,
            }
        else:
            log.error("Execution failed: %s", str(result["data"])[:200])
            return {
                "rows": None,
                "execution_status": "FAILED",
                "error": str(result["data"])[:500],
                "result_data": None,
            }

    except Exception as e:
        log.error("Execution exception: %s", str(e)[:200])
        return {
            "rows": None,
            "execution_status": "FAILED",
            "error": str(e)[:500],
            "result_data": None,
        }
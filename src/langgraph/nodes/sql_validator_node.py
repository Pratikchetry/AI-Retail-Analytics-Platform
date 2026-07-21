"""
Phase 1 — AI Retail Intelligence Platform
SQL Validator Node.

Wraps the existing ValidationAgent. Returns is_valid + errors so the
graph can decide whether to retry or skip execution.
"""

from src.agent.validation_agent import ValidationAgent
from src.utils.logger import get_logger
from src.langgraph.state import AgentState

log = get_logger(__name__)


def sql_validator_node(state: AgentState) -> dict:
    """Validate generated SQL against safety and schema rules."""
    sql = state.get("sql", "")
    question = state.get("question", "")
    context = state.get("context", "")

    log.info("Validating SQL: %s", sql[:80] if sql else "EMPTY")

    validator = ValidationAgent()
    result = validator.validate(sql, question, context)

    is_valid = result.is_valid if hasattr(result, "is_valid") else False
    errors = list(result.errors) if hasattr(result, "errors") else []
    warnings = list(result.warnings) if hasattr(result, "warnings") else []

    log.info("Validation: is_valid=%s errors=%d warnings=%d",
             is_valid, len(errors), len(warnings))

    return {
        "is_valid": is_valid,
        "validation_errors": errors,
        "validation_warnings": warnings,
    }
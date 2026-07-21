"""
Phase 1 — AI Retail Intelligence Platform
Reasoning Node.

Wraps the existing BusinessReasoningAgent. Enforces the evidence hierarchy:
SQL execution result is ground truth; knowledge base is supporting context.
"""

from src.agent.business_reasoning_agent import BusinessReasoningAgent
from src.utils.logger import get_logger
from src.langgraph.state import AgentState

log = get_logger(__name__)


def reasoning_node(state: AgentState) -> dict:
    """Synthesize a business answer from SQL result + context."""
    question = state["question"]
    context = state.get("context", "")
    rows = state.get("rows", "")

    log.info("Reasoning for: '%s'", question[:60])

    reasoning_agent = BusinessReasoningAgent()
    result = reasoning_agent.reason(question, context, sql_result=rows)

    log.info("Reasoning answer: %s", result.answer[:100] if result.answer else "EMPTY")

    return {
        "answer": result.answer,
        "reasoning": result.reasoning,
        "evidence": result.evidence,
    }
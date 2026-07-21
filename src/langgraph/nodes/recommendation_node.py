"""
Phase 1 — AI Retail Intelligence Platform
Recommendation Node.

Takes the reasoning output and generates a concrete, actionable business
recommendation. This is the 'so what / do this' layer that turns an
insight into a decision.
"""

from src.llm.local_llm import LocalLLM
from src.utils.logger import get_logger
from src.langgraph.state import AgentState

log = get_logger(__name__)


def recommendation_node(state: AgentState) -> dict:
    """Generate a business recommendation from the answer."""
    question = state.get("question", "")
    answer = state.get("answer", "")
    route = state.get("route", "")

    log.info("Recommendation for: '%s'", question[:60])

    # Out-of-scope and unavailable cases don't get recommendations
    if route == "OUT_OF_SCOPE":
        return {"recommendation": "No recommendation — question outside warehouse scope."}

    rows = state.get("rows", "")
    if rows == "INFORMATION_NOT_AVAILABLE" or "not available" in answer.lower():
        return {"recommendation": "No recommendation — information not available in the warehouse."}

    llm = LocalLLM()

    prompt = f"""You are a Senior Retail Revenue Strategist.

Based on the analysis below, give ONE concrete, actionable business recommendation.
Be specific and practical — name the segment, product, or time window involved.
Keep it to 2-3 sentences. Do NOT invent numbers not present in the analysis.

QUESTION: {question}
ANALYSIS: {answer}

If the analysis genuinely does not support a recommendation (e.g. it's a simple
lookup like "what is the total revenue"), say:
"No action required — informational query."

RECOMMENDATION:"""

    try:
        rec = llm.generate(prompt).strip()
    except Exception as e:
        log.error("Recommendation LLM call failed: %s", e)
        rec = "Recommendation unavailable."

    log.info("Recommendation: %s", rec[:100])
    return {"recommendation": rec}
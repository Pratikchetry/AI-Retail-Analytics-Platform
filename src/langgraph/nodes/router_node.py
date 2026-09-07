"""
Phase 1 — AI Retail Intelligence Platform
Router Node.

Uses the LLM to classify a question into one of five routes. This replaces
the brittle keyword-based IntentAgent and the hardcoded out-of-scope checks
(BusinessValidator / ExecutionValidator) with a single generalizable classifier.

LLM is instantiated once at module level (not per call) to avoid
repeated client initialization overhead on every request.
"""

from src.llm.local_llm import LocalLLM
from src.utils.logger import get_logger
from src.langgraph.state import AgentState

log = get_logger(__name__)

# Instantiated once at import time — shared across all calls
# Uses the fast 20B model (gpt-oss-20b) for classification
_llm = LocalLLM(model_size="8b")

VALID_ROUTES = {"SQL_LOOKUP", "FORECAST", "ANOMALY", "METADATA", "OUT_OF_SCOPE"}

ROUTER_PROMPT = """You are a routing agent for a UK retail revenue intelligence system.

Classify the user's question into EXACTLY ONE of these routes:

1. SQL_LOOKUP      — The question can be answered by querying the PostgreSQL
                     data warehouse. Examples: revenue totals, top products,
                     customer segments, country comparisons, monthly growth,
                     year-over-year analysis, average order value.

2. FORECAST        — The question asks to predict or project FUTURE revenue
                     or trends. Examples: "forecast next month", "predict
                     revenue", "what will revenue be next quarter".

3. ANOMALY         — The question is about unusual events, spikes, drops,
                     or outliers in the data. Examples: "what are the anomalies",
                     "any unusual revenue days", "detect spikes".

4. METADATA        — The question is about a KNOWN BUSINESS FACT that lives in
                     the knowledge base and does NOT need a database query.
                     Examples: "what is the superstar product", "why did YoY
                     decline", "what is the operationally critical month".

5. OUT_OF_SCOPE    — The question asks about something NOT in this retail
                     data warehouse at all. Examples: TikTok advertising,
                     social media, competitor analysis, employee salaries,
                     weather data, stock prices.

Return ONLY the route name, nothing else. No explanation. No punctuation.
"""

# Signals that strongly indicate a METADATA answer exists in the knowledge base
_METADATA_SIGNALS = [
    "superstar product",
    "only true superstar",
    "operationally critical",
    "non-negotiable peak",
    "why did yoy",
    "negative yoy",
    "partial month",
    "peak month",
    "yoy growth decline",
    "yoy show negative",
    "paper craft little birdie",
    "cream hanging heart",
]

# Signals that indicate the question is outside the warehouse scope
_OUT_OF_SCOPE_SIGNALS = [
    "tiktok",
    "facebook ads",
    "google ads",
    "instagram",
    "social media",
    "advertising revenue",
    "competitor",
    "stock price",
    "stock market",
    "employee salary",
    "weather",
    "cryptocurrency",
    "bitcoin",
    "news",
    "sports",
]


def _classify(question: str) -> str:
    """
    Ask the LLM to classify the question route.
    Falls back to SQL_LOOKUP on any failure.
    """
    try:
        raw = _llm.generate(
            f"{ROUTER_PROMPT}\n\nQuestion: {question}\n\nRoute:"
        )
        if not raw or not raw.strip():
            log.warning("Router returned empty response — defaulting to SQL_LOOKUP")
            return "SQL_LOOKUP"

        # Take the first word and clean punctuation
        route = raw.strip().upper().split()[0].strip(".:,;\"'")

        if route not in VALID_ROUTES:
            log.warning(
                "Router returned unknown route '%s' — defaulting to SQL_LOOKUP", route
            )
            return "SQL_LOOKUP"

        return route

    except Exception as e:
        log.error("Router LLM call failed: %s — defaulting to SQL_LOOKUP", str(e)[:120])
        return "SQL_LOOKUP"


def router_node(state: AgentState) -> dict:
    """
    Entry point node: classify the user question into a route.

    Returns:
        route: one of SQL_LOOKUP | FORECAST | ANOMALY | METADATA | OUT_OF_SCOPE
        attempt: reset to 0 for each new question
        max_attempts: maximum SQL retry attempts allowed
    """
    question = state.get("question", "").strip()

    if not question:
        log.warning("Router received empty question — defaulting to OUT_OF_SCOPE")
        return {
            "route": "OUT_OF_SCOPE",
            "attempt": 0,
            "max_attempts": 3,
        }

    # Get LLM classification
    route = _classify(question)

    # Apply heuristic guardrails on top of LLM (defense in depth)
    q_lower = question.lower()

    # Override to METADATA if strong signals are present
    if route == "SQL_LOOKUP" and any(s in q_lower for s in _METADATA_SIGNALS):
        route = "METADATA"
        log.info("Router: metadata signal detected — overriding to METADATA")

    # Override to OUT_OF_SCOPE if strong signals are present
    # (applies regardless of LLM classification)
    if any(s in q_lower for s in _OUT_OF_SCOPE_SIGNALS):
        route = "OUT_OF_SCOPE"
        log.info("Router: out-of-scope signal detected — overriding to OUT_OF_SCOPE")

    log.info("Router: '%s...' -> %s", question[:60], route)

    return {
        "route": route,
        "attempt": 0,
        "max_attempts": 3,
    }
"""
Phase 1 — AI Retail Intelligence Platform
Router Node.

Uses the LLM to classify a question into one of five routes. This replaces
the brittle keyword-based IntentAgent and the hardcoded out-of-scope checks
(BusinessValidator / ExecutionValidator) with a single generalizable classifier.
"""

from src.llm.local_llm import LocalLLM
from src.utils.logger import get_logger
from src.langgraph.state import AgentState

log = get_logger(__name__)

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

Return ONLY the route name, nothing else.
"""


def _classify(question: str, llm: LocalLLM) -> str:
    """Ask the LLM to classify, with a safe fallback."""
    try:
        raw = llm.generate(f"{ROUTER_PROMPT}\n\nQuestion: {question}\n\nRoute:")
        route = raw.strip().upper().split()[0] if raw.strip() else ""
        # Strip any punctuation the LLM might add
        route = route.strip(".:,;")
        if route not in VALID_ROUTES:
            log.warning("Router returned unknown route '%s' — defaulting to SQL_LOOKUP", route)
            return "SQL_LOOKUP"
        return route
    except Exception as e:
        log.error("Router LLM call failed: %s — defaulting to SQL_LOOKUP", e)
        return "SQL_LOOKUP"


def router_node(state: AgentState) -> dict:
    """Entry point: classify the question's route."""
    question = state["question"]
    llm = LocalLLM()

    route = _classify(question, llm)

    # Quick heuristic guardrails on top of the LLM (defense in depth)
    q_lower = question.lower()
    if route == "SQL_LOOKUP":
        # These strong signals override into METADATA / OUT_OF_SCOPE
        metadata_signals = [
            "superstar product", "only true superstar",
            "operationally critical", "non-negotiable peak",
            "why did yoy", "negative yoy", "partial month",
        ]
        if any(s in q_lower for s in metadata_signals):
            route = "METADATA"

    out_of_scope_signals = [
        "tiktok", "facebook ads", "google ads", "social media",
        "advertising revenue", "competitor", "stock price",
        "employee salary", "weather",
    ]
    if any(s in q_lower for s in out_of_scope_signals):
        route = "OUT_OF_SCOPE"

    log.info("Router: '%s' -> %s", question[:60], route)

    return {
        "route": route,
        "attempt": 0,
        "max_attempts": 3,
    }
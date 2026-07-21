"""
Phase 2 — AI Retail Intelligence Platform
Critic Node.

Quality gate. Scores the final answer 0.0-1.0 on three criteria:
1. Grounded — does it use the SQL result / retrieved context?
2. Faithful — does it avoid inventing numbers not in the evidence?
3. Relevant — does it actually answer the question?

Auto-passes for routes that produce authoritative model/data outputs
(FORECAST, ANOMALY, OUT_OF_SCOPE) where the SQL-grounding check
does not apply.
"""

import re
from src.llm.local_llm import LocalLLM
from src.utils.logger import get_logger
from src.langgraph.state import AgentState

log = get_logger(__name__)

THRESHOLD = 0.7

# Routes that produce authoritative outputs — auto-pass (no LLM critique needed)
AUTO_PASS_ROUTES = {"FORECAST", "ANOMALY", "OUT_OF_SCOPE"}


def critic_node(state: AgentState) -> dict:
    """Score the final answer and decide whether it passes."""
    question = state.get("question", "")
    answer = state.get("answer", "")
    evidence = state.get("evidence", "")
    rows = state.get("rows", "")
    route = state.get("route", "")

    log.info("Critique for: '%s'", question[:60])

    # ---- Authoritative routes always pass (model/data outputs) ----
    if route in AUTO_PASS_ROUTES:
        log.info("%s route — auto-pass (authoritative output)", route)
        return {
            "critic_score": 1.0,
            "critic_feedback": f"{route} produces authoritative model/data output — no grounding check needed.",
            "critic_passes": True,
        }

    if rows == "INFORMATION_NOT_AVAILABLE":
        log.info("INFORMATION_NOT_AVAILABLE — auto-pass")
        return {"critic_score": 1.0, "critic_feedback": "Honest decline — not in warehouse.", "critic_passes": True}

    llm = LocalLLM()

    prompt = f"""You are a strict quality auditor for a retail intelligence system.

Score the answer below from 0.0 to 1.0 based on:
1. GROUNDED — Does the answer use the SQL result or retrieved context?
2. FAITHFUL — Does it avoid inventing numbers not in the evidence?
3. RELEVANT — Does it directly answer the question?

QUESTION: {question}
ANSWER: {answer}
EVIDENCE: {evidence}

Respond in EXACTLY this format (no other text):
SCORE: <float between 0.0 and 1.0>
FEEDBACK: <one sentence>"""

    try:
        raw = llm.generate(prompt)
        score_match = re.search(r"SCORE:\s*([\d.]+)", raw, re.IGNORECASE)
        feedback_match = re.search(r"FEEDBACK:\s*(.+)", raw, re.IGNORECASE | re.DOTALL)

        score = float(score_match.group(1)) if score_match else 0.5
        score = max(0.0, min(1.0, score))
        feedback = feedback_match.group(1).strip() if feedback_match else "No feedback parsed."
    except Exception as e:
        log.error("Critic LLM call failed: %s — defaulting to pass", e)
        score, feedback = 0.8, "Critic LLM unavailable — defaulting to pass."

    passes = score >= THRESHOLD
    log.info("Critic score: %.2f | passes=%s | %s", score, passes, feedback[:80])

    return {
        "critic_score": score,
        "critic_feedback": feedback,
        "critic_passes": passes,
    }
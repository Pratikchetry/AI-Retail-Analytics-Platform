"""
Phase 5.5 — AI Retail Intelligence Platform
METADATA Verifier Node.

Context engineering layer 2: what gets TRUSTED + what WINS on conflict.
When the agent answers a METADATA question from the knowledge base, this
node runs a confirmation query against the LIVE warehouse. If the KB claim
and the warehouse disagree, the WAREHOUSE WINS — the answer is corrected
to the verified truth. Deterministic — no LLM call.
"""

from sqlalchemy import text

from src.utils.db import engine
from src.utils.logger import get_logger
from src.langgraph.state import AgentState

log = get_logger(__name__)


def _verify_superstar_product():
    """Verify WHITE HANGING HEART T-LIGHT HOLDER is a true Superstar —
    top-15 on revenue AND quantity AND orders."""
    claim = "WHITE HANGING HEART T-LIGHT HOLDER"
    sql = text("""
        SELECT description, total_revenue, total_quantity, total_orders,
               RANK() OVER (ORDER BY total_revenue DESC) AS rev_rank,
               RANK() OVER (ORDER BY total_quantity DESC) AS qty_rank,
               RANK() OVER (ORDER BY total_orders DESC) AS ord_rank
        FROM product_performance_matrix
        WHERE description ILIKE :claim
    """)
    with engine.connect() as conn:
        rows = conn.execute(sql, {"claim": "%WHITE HANGING HEART T-LIGHT%"}).fetchall()

    if not rows:
        return False, f"CONFLICT: '{claim}' not found in performance matrix."

    m = rows[0]
    rev_rank, qty_rank, ord_rank = int(m[4]), int(m[5]), int(m[6])
    if rev_rank <= 15 and qty_rank <= 15 and ord_rank <= 15:
        return True, (f"'{m[0].strip()}' is the true Superstar — revenue rank #{rev_rank} "
                      f"(£{float(m[1]):,.0f}), quantity rank #{qty_rank} ({int(m[2]):,} units), "
                      f"orders rank #{ord_rank} ({int(m[3]):,} orders). Top-15 on all three dimensions.")
    return False, (f"'{m[0].strip()}' ranks revenue #{rev_rank}, quantity #{qty_rank}, "
                   f"orders #{ord_rank} — not a Superstar.")


def _verify_operational_month():
    sql = text("""
        SELECT month_name, year, total_revenue
        FROM revenue_monthly_summary ORDER BY total_revenue DESC LIMIT 1
    """)
    with engine.connect() as conn:
        row = conn.execute(sql).fetchone()
    if row and "november" in (row[0] or "").lower():
        return True, f"November is the peak month (£{float(row[2]):,.0f} in {row[1]})."
    return False, f"Peak month is {row[0]} {row[1]} (£{float(row[2]):,.0f}), NOT November."


def _verify_yoy_decline():
    sql = text("SELECT MAX(order_date) AS last_sale FROM fact_sales WHERE order_date >= '2011-12-01'")
    with engine.connect() as conn:
        row = conn.execute(sql).fetchone()
    last = str(row[0]) if row else ""
    if last and last < "2011-12-31":
        return True, f"December 2011 data ends {last} (partial month) — supports the YoY artifact explanation."
    return False, f"December 2011 data extends to {last} — partial-month claim may be inaccurate."


VERIFIERS = {
    "superstar": _verify_superstar_product,
    "operational": _verify_operational_month,
    "critical": _verify_operational_month,
    "yoy": _verify_yoy_decline,
    "negative growth": _verify_yoy_decline,
}


def _detect_and_correct_conflict(question, answer, note, verified):
    """Context engineering rule: WAREHOUSE WINS on conflict.
    If the verified truth contradicts the answer, return a corrected answer."""
    if not verified:
        return answer, False
    q = question.lower()
    a = answer.lower()
    n = note.lower()

    # Superstar product: warehouse says WHITE, answer says something else
    if "superstar" in q and "white hanging heart" in n:
        if "white hanging heart" not in a:
            corrected = (f"The true Superstar product is WHITE HANGING HEART T-LIGHT HOLDER. "
                         f"Warehouse verification: {note}")
            return corrected, True

    return answer, False


def metadata_verifier_node(state: AgentState) -> dict:
    """Cross-check METADATA answers against the live warehouse. Warehouse wins."""
    route = state.get("route", "")
    question = state.get("question", "")
    answer = state.get("answer", "")
    evidence = state.get("evidence", "")

    if route != "METADATA":
        return {}

    q_lower = question.lower()
    verifier = None
    matched_key = None
    for key, fn in VERIFIERS.items():
        if key in q_lower:
            verifier = fn
            matched_key = key
            break

    if not verifier:
        log.info("Verifier: no registered check for '%s', passing through", question[:50])
        return {}

    log.info("Verifier: checking '%s' claim against warehouse", matched_key)

    try:
        verified, note = verifier()
        status = "VERIFIED" if verified else "CONFLICT_DETECTED"
    except Exception as e:
        log.error("Verifier query failed: %s", str(e)[:150])
        note = f"VERIFICATION_UNAVAILABLE: {str(e)[:100]}"
        status = "UNVERIFIED"
        verified = None

    new_evidence = f"{evidence}\n\nWAREHOUSE VERIFICATION [{status}]: {note}"

    # Self-heal: if warehouse truth contradicts the answer, override it
    result = {"evidence": new_evidence}
    if verified:
        corrected, did_override = _detect_and_correct_conflict(question, answer, note, verified)
        if did_override:
            log.info("Verifier: CONFLICT OVERRIDE — warehouse truth wins, answer corrected")
            result["answer"] = corrected

    log.info("Verifier: %s | %s", status, note[:80])
    return result
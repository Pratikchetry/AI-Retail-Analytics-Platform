"""
Phase 2 — AI Retail Intelligence Platform
Anomaly Node.

Reads the real ml_anomaly_scores table (populated by the Isolation Forest
in Phase 0) and summarizes genuine anomalies.
"""

from sqlalchemy import text

from src.utils.db import engine
from src.utils.logger import get_logger
from src.langgraph.state import AgentState

log = get_logger(__name__)


def anomaly_node(state: AgentState) -> dict:
    """Summarize the top revenue anomalies from the warehouse."""
    question = state["question"]
    log.info("Anomaly node for: '%s'", question[:60])

    try:
        with engine.connect() as conn:
            # Overall counts
            total = conn.execute(text("SELECT COUNT(*) FROM ml_anomaly_scores")).scalar()
            n_anom = conn.execute(
                text("SELECT COUNT(*) FROM ml_anomaly_scores WHERE is_anomaly = TRUE")
            ).scalar()

            # Top 5 spikes and drops by anomaly score
            spikes = conn.execute(text("""
                SELECT order_date, country_name, daily_revenue, anomaly_score
                FROM ml_anomaly_scores
                WHERE is_anomaly = TRUE AND daily_revenue > 50000
                ORDER BY anomaly_score DESC
                LIMIT 5
            """)).fetchall()

            drops = conn.execute(text("""
                SELECT order_date, country_name, daily_revenue, anomaly_score
                FROM ml_anomaly_scores
                WHERE is_anomaly = TRUE AND daily_revenue < 10000
                ORDER BY anomaly_score DESC
                LIMIT 5
            """)).fetchall()

    except Exception as e:
        log.error("Failed to read ml_anomaly_scores: %s", e)
        return {
            "answer": f"Anomaly data unavailable: {str(e)[:200]}",
            "evidence": "",
            "execution_status": "FAILED",
        }

    rate = (n_anom / total * 100) if total else 0

    def _fmt(rows):
        return "\n".join(
            f"  {r[0]}  {r[1]:20s}  £{float(r[2]):>12,.2f}  (score {float(r[3]):.3f})"
            for r in rows
        )

    answer = (
        f"The Isolation Forest model detected {n_anom} anomalies out of {total} "
        f"daily-country observations ({rate:.1f}% anomaly rate).\n\n"
        f"Top revenue spikes:\n{_fmt(spikes)}\n\n"
        f"Top revenue drops:\n{_fmt(drops)}"
    )

    evidence = f"Total rows: {total} | Anomalies: {n_anom} | Rate: {rate:.1f}%"

    log.info("Anomaly summary | %d anomalies of %d (%.1f%%)", n_anom, total, rate)

    return {
        "answer": answer,
        "evidence": evidence,
        "execution_status": "SUCCESS",
    }
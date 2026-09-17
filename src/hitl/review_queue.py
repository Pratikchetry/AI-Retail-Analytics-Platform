"""
Human-in-the-Loop review queue.

Hooked into run_agent(): any answer that exhausted its retry budget while
still failing the critic gets logged here instead of silently returned to
the user with no distinction from a passing answer.
"""
from sqlalchemy import text
from src.utils.db import engine
from src.utils.logger import get_logger

log = get_logger(__name__)


def flag_for_review(question: str, result: dict) -> None:
    """Insert a low-confidence, retry-exhausted answer into the review queue."""
    try:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO human_review_queue
                        (question, answer, route, critic_score, critic_feedback,
                         sql_generated, evidence)
                    VALUES
                        (:question, :answer, :route, :critic_score, :critic_feedback,
                         :sql_generated, :evidence)
                """),
                {
                    "question": question,
                    "answer": result.get("answer", ""),
                    "route": result.get("route", ""),
                    "critic_score": result.get("critic_score", 0.0),
                    "critic_feedback": result.get("critic_feedback", ""),
                    "sql_generated": result.get("sql", ""),
                    "evidence": result.get("evidence", ""),
                },
            )
        log.warning(
            "HITL: flagged for review — score=%.2f question='%s'",
            result.get("critic_score", 0.0), question[:60],
        )
    except Exception as e:
        # Never let review-queue logging break the actual user-facing response
        log.error("HITL: failed to flag for review: %s", str(e)[:200])


def get_pending_reviews(limit: int = 50) -> list[dict]:
    """Fetch unreviewed entries, most recent first."""
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT id, question, answer, route, critic_score, critic_feedback,
                       sql_generated, evidence, created_at
                FROM human_review_queue
                WHERE reviewed = FALSE
                ORDER BY created_at DESC
                LIMIT :limit
            """),
            {"limit": limit},
        ).mappings().all()
    return [dict(r) for r in rows]


def resolve_review(review_id: int, reviewer_notes: str, corrected_answer: str = None) -> bool:
    """Mark a review as resolved, with optional notes and a corrected answer."""
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE human_review_queue
                SET reviewed = TRUE,
                    reviewer_notes = :notes,
                    corrected_answer = :corrected,
                    reviewed_at = NOW()
                WHERE id = :id
            """),
            {"id": review_id, "notes": reviewer_notes, "corrected": corrected_answer},
        )
    return result.rowcount > 0
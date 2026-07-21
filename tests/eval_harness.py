"""
Phase 5 — Evaluation Harness (free-tier safe).

Treats Groq rate-limit failures as SKIP (excluded from the pass-rate
denominator) so the score measures AGENT QUALITY, not throughput.

Run: PYTHONPATH=. python tests/eval_harness.py
"""

import sys
import time

from src.langgraph.graph import run_agent
from src.utils.logger import get_logger

log = get_logger(__name__)

# 12 questions across all 5 routes — fits a free-tier window
QUESTIONS = [
    # SQL_LOOKUP (4)
    ("Which country had the highest average order value?", "SQL_LOOKUP"),
    ("What were the total sales in Germany?", "SQL_LOOKUP"),
    ("Name the top 3 products by revenue.", "SQL_LOOKUP"),
    ("What is the total revenue?", "SQL_LOOKUP"),
    # METADATA (2)
    ("What is the only true Superstar product?", "METADATA"),
    ("What month is operationally critical?", "METADATA"),
    # FORECAST (2)
    ("Forecast revenue for the next 14 days", "FORECAST"),
    ("What will revenue be next week?", "FORECAST"),
    # ANOMALY (2)
    ("What are the recent revenue anomalies?", "ANOMALY"),
    ("Any revenue spikes detected?", "ANOMALY"),
    # OUT_OF_SCOPE (2)
    ("What was TikTok advertising revenue?", "OUT_OF_SCOPE"),
    ("What is the stock price?", "OUT_OF_SCOPE"),
]

THRESHOLD = 0.70

RATE_LIMIT_MARKERS = ("429", "rate limit", "too many requests", "max retries exceeded")


def run_one(question, expected_route):
    """Returns dict: passed, route_correct, score, status (PASS/FAIL/SKIP)."""
    try:
        result = run_agent(question)
        passed = result.get("critic_passes", False)
        got_route = result.get("route", "")
        return {
            "passed": passed,
            "route_correct": got_route == expected_route,
            "score": result.get("critic_score", 0.0),
            "status": "PASS" if passed else "FAIL",
            "got_route": got_route,
        }
    except Exception as e:
        msg = str(e).lower()
        log.error("Question errored: '%s' -> %s", question[:50], str(e)[:150])
        # Rate-limit failures are infrastructure, not quality -> SKIP
        if any(m in msg for m in RATE_LIMIT_MARKERS):
            return {"passed": False, "route_correct": False, "score": 0.0,
                    "status": "SKIP", "got_route": "RATE_LIMITED"}
        return {"passed": False, "route_correct": False, "score": 0.0,
                "status": "FAIL", "got_route": "ERROR"}


def main():
    print("=" * 90)
    print("EVALUATION HARNESS — free-tier safe (rate-limit = SKIP)")
    print("=" * 90)
    print(f"{'#':>3}  {'ROUTE':>6}  {'SCORE':>6}  {'ST':>5}  QUESTION")
    print("-" * 90)

    passed = 0
    route_ok = 0
    skipped = 0
    scored = 0
    start = time.time()

    for i, (question, expected_route) in enumerate(QUESTIONS, 1):
        r = run_one(question, expected_route)

        if r["status"] != "SKIP":
            scored += 1
            if r["passed"]:
                passed += 1
            if r["route_correct"]:
                route_ok += 1
        else:
            skipped += 1

        rflag = "OK" if r["route_correct"] else "NO"
        print(f"{i:>3}  {rflag:>6}  {r['score']:>6.2f}  {r['status']:>5}  {question[:55]}")

        # Cooldown to respect free-tier limits (skip after last)
        if i < len(QUESTIONS):
            time.sleep(12)

    elapsed = time.time() - start
    pass_rate = (passed / scored) if scored else 0.0
    route_rate = (route_ok / scored) if scored else 0.0

    print("-" * 90)
    print(f"Scored questions:  {scored}/{len(QUESTIONS)}  ({skipped} skipped for rate limits)")
    print(f"Critic passed:     {passed}/{scored}  ({pass_rate:.1%})")
    print(f"Route accuracy:    {route_ok}/{scored}  ({route_rate:.1%})")
    print(f"Time:              {elapsed:.0f}s")
    print("=" * 90)

    if scored == 0:
        print("RESULT: INCONCLUSIVE — all questions rate-limited. Retry later.")
        sys.exit(2)
    if pass_rate >= THRESHOLD:
        print(f"RESULT: PASS  (>= {THRESHOLD:.0%} threshold)")
        sys.exit(0)
    print(f"RESULT: FAIL  (< {THRESHOLD:.0%} threshold)")
    sys.exit(1)


if __name__ == "__main__":
    main()
"""
Phase 2 — Full LangGraph agent integration test.
Covers SQL_LOOKUP, OUT_OF_SCOPE, FORECAST, and ANOMALY routes.
"""

from src.langgraph.graph import run_agent


def run(question: str):
    print(f"\n{'='*80}")
    print(f"Q: {question}")
    print("=" * 80)

    result = run_agent(question)

    print(f"\nRoute:          {result.get('route', '?')}")
    print(f"Exec status:    {result.get('execution_status', '?')}")
    print(f"\n--- ANSWER ---\n{result.get('answer', '(none)')}")
    print(f"\n--- RECOMMENDATION ---\n{result.get('recommendation', '(none)')}")
    print(f"\n--- CRITIC ---\nScore: {result.get('critic_score', 0):.2f} | "
          f"Passes: {result.get('critic_passes', False)}")
    return result


def main():
    questions = [
        # SQL route
        "Which country had the highest average order value?",
        # Out of scope
        "What was TikTok advertising revenue?",
        # FORECAST route — real model
        "Forecast revenue for the next 14 days",
        # ANOMALY route — real Isolation Forest
        "What are the recent revenue anomalies?",
    ]

    results = []
    for q in questions:
        r = run(q)
        results.append((q, r.get("critic_score", 0), r.get("critic_passes", False)))

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    passed = 0
    for q, score, ok in results:
        flag = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        print(f"  [{flag}] {score:.2f}  {q[:55]}")
    print(f"\n{passed}/{len(questions)} passed the critic gate.")


if __name__ == "__main__":
    main()
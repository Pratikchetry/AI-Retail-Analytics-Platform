"""
Quick router sanity test — run before building the full graph.
"""

from src.langgraph.nodes.router_node import router_node


def main():
    test_cases = [
        ("Which country had the highest average order value in Q3 2011?", "SQL_LOOKUP"),
        ("What was TikTok advertising revenue?", "OUT_OF_SCOPE"),
        ("What is the only true Superstar product?", "METADATA"),
        ("Why did YoY show negative growth?", "METADATA"),
        ("Forecast revenue for the next 14 days", "FORECAST"),
        ("What are the recent revenue anomalies?", "ANOMALY"),
        ("Which customer segment generates the most revenue?", "SQL_LOOKUP"),
        ("How much did we spend on Facebook ads?", "OUT_OF_SCOPE"),
        ("What month had the highest revenue?", "SQL_LOOKUP"),
        ("What is customer lifetime value?", "SQL_LOOKUP"),
    ]

    print(f"{'QUESTION':60s} {'EXPECTED':15s} {'GOT':15s} {'OK'}")
    print("-" * 100)

    correct = 0
    for question, expected in test_cases:
        result = router_node({"question": question})
        got = result["route"]
        ok = "✅" if got == expected else "❌"
        if got == expected:
            correct += 1
        print(f"{question[:60]:60s} {expected:15s} {got:15s} {ok}")

    print("-" * 100)
    print(f"Score: {correct}/{len(test_cases)}")


if __name__ == "__main__":
    main()
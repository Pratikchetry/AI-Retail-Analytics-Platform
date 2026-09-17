"""
Latency Benchmark — Retail Revenue Intelligence API (/ask endpoint)
Correctly uses the real AskRequest schema: {"question": "..."}

Separates COLD latency (first time a question is asked, full pipeline runs)
from CACHED latency (identical question asked again within the 10-minute
cache TTL) — mixing these would produce a misleading percentile, since
they are fundamentally different code paths.

Run: python3 benchmark_latency.py
"""
import time
import statistics
import requests

API_URL = "https://retail-ai-api-pratik-g9fje5ayeyc8cpgm.koreacentral-01.azurewebsites.net/ask"

QUESTIONS = [
    "What is the total revenue?",
    "Which customer segment generates most revenue?",
    "What is the only true Superstar product?",
    "What month is operationally critical?",
    "Why did YoY show negative growth?",
]

CACHE_PASSES = 3  # after the cold pass, repeat verbatim this many times to measure cache-hit latency
TIMEOUT_S = 180  # increased from 90s to distinguish "very slow but working" from "genuinely stuck"


def call(question: str):
    start = time.monotonic()
    try:
        resp = requests.post(API_URL, json={"question": question}, timeout=TIMEOUT_S)
        elapsed = time.monotonic() - start
        if resp.status_code == 200:
            data = resp.json()
            route = data.get("route", "UNKNOWN")
            return {"ok": True, "elapsed": elapsed, "route": route, "status": 200}
        else:
            return {"ok": False, "elapsed": elapsed, "status": resp.status_code, "body": resp.text[:200]}
    except requests.exceptions.RequestException as e:
        elapsed = time.monotonic() - start
        return {"ok": False, "elapsed": elapsed, "status": None, "body": f"{type(e).__name__}: {e}"}


def summarize(label, latencies):
    if not latencies:
        print(f"{label}: no successful samples")
        return
    s = sorted(latencies)
    n = len(s)
    p50 = s[int(n * 0.50)]
    p95 = s[min(int(n * 0.95), n - 1)]
    print(f"\n{label} (n={n})")
    print(f"  min:    {min(s):.2f}s")
    print(f"  max:    {max(s):.2f}s")
    print(f"  mean:   {statistics.mean(s):.2f}s")
    print(f"  p50:    {p50:.2f}s")
    print(f"  p95:    {p95:.2f}s")


def run_benchmark():
    cold_latencies = []
    cache_latencies = []
    errors = []

    print(f"COLD pass — one fresh call per question ({len(QUESTIONS)} requests)\n")
    for q in QUESTIONS:
        r = call(q)
        if r["ok"]:
            cold_latencies.append(r["elapsed"])
            print(f"  {r['elapsed']:.2f}s  route={r['route']:<10}  {q[:45]}")
        else:
            errors.append(f"COLD  HTTP {r['status']}: {q}  -> {r.get('body','')}")
            print(f"  FAIL ({r['status']})  {q[:45]}  -> {r.get('body','')}")

    print(f"\nCACHE passes — repeating the same questions verbatim ({CACHE_PASSES}x each)\n")
    for i in range(CACHE_PASSES):
        for q in QUESTIONS:
            r = call(q)
            if r["ok"]:
                cache_latencies.append(r["elapsed"])
                print(f"  [{i+1}] {r['elapsed']:.2f}s  route={r['route']:<10}  {q[:45]}")
            else:
                errors.append(f"CACHE HTTP {r['status']}: {q}  -> {r.get('body','')}")
                print(f"  [{i+1}] FAIL ({r['status']})  {q[:45]}  -> {r.get('body','')}")

    print("\n" + "=" * 55)
    print("LATENCY BENCHMARK RESULTS")
    print("=" * 55)
    summarize("COLD (full pipeline, cache miss)", cold_latencies)
    summarize("CACHED (served from in-memory cache)", cache_latencies)

    total = len(QUESTIONS) + len(QUESTIONS) * CACHE_PASSES
    print(f"\nError rate: {len(errors)}/{total} ({100*len(errors)/total:.1f}%)")
    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  - {e}")
    print("=" * 55)


if __name__ == "__main__":
    run_benchmark()
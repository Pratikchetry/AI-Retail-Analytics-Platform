# Reliability, Latency & Failure Recovery — Verified Findings

Every number and claim below comes from an actual run against the live Azure
deployment or from real timestamps in production logs, captured during a
live debugging session. Sample sizes are small — this is a first pass, not
a large-scale benchmark — and that's stated honestly rather than implied
otherwise.

## 1. Latency (real measurements, `/ask` endpoint)

| Path | n | min | max | mean | p50 | p95 |
|---|---|---|---|---|---|---|
| Full pipeline (cache miss) | 3–5 across runs | 6.2s | 79.5s | ~20–37s | ~18–37s | ~30–79s |
| Cached response | 14–15 across runs | 0.7s | 12.5s | ~2–3s | ~1–1.7s | ~2–12.5s |

**Honest caveats:**
- Sample sizes are single digits for the cold path — not enough to trust a stable p95. Variance between runs was large (25s to 79s for the same p50 slot), driven mostly by whether Groq happened to be rate-limited at that moment.
- One run's "cold" measurements were contaminated by a leftover cache from a prior run (10-minute TTL) — a real methodology mistake, disclosed rather than hidden.
- Cache hits are consistently ~10–20x faster than a fresh pipeline run.

## 2. Bottleneck breakdown (from one real, timestamped production trace)

Extracted from actual log timestamps for one full question, including a
critic-triggered retry:

| Stage | Time |
|---|---|
| Router (LLM call) | ~5.3s |
| RAG retrieval | ~0.12s |
| Context compression | <0.01s |
| SQL generation (LLM call) | ~3.0s |
| SQL execution (Neon) | ~4.7–7.0s |
| Reasoning (LLM call) | ~2.1–2.4s |
| Recommendation (LLM call) | ~1.1–1.4s |
| Critic (LLM call) | ~1.3s |
| **Groq 429 backoff wait (when it occurs)** | **up to ~29–33s per occurrence** |

**Two genuine bottlenecks identified:**
1. **Groq rate-limit backoff is the single largest cost by far** — a single backoff wait (29–33s) exceeded the entire rest of the pipeline combined. This is a direct, structural consequence of running on Groq's free tier under load.
2. **SQL execution against Neon (4.7–7.0s)** for a single-row aggregate query is unusually slow — likely a serverless connection/cold-start cost on Neon's side, not query complexity. Not yet root-caused; flagged as a real open question, not solved.

## 3. Failure recovery — what actually exists now (verified, not aspirational)

**Before this session:** `LocalLLM` had zero fallback. Any Groq failure (429, timeout) raised `RuntimeError` and killed the entire agent request with a `500`. The README's "LLM Router: Gemini primary + Groq fallback" claim was false — `GeminiClient` existed as dead code, never imported by `LocalLLM`.

**What was built and verified working:**
- **Real Groq → Gemini fallback**: confirmed via a standalone test (`200 OK`, real response) and via production logs after deploy.
- **In-process circuit breaker**: after 3 consecutive Groq failures, Groq is skipped entirely for a 60-second cooldown, going straight to Gemini instead of waiting through Groq's own retry backoff on every call.
- **Explicit scope limit, stated plainly**: this breaker is in-memory, per-process. It resets on restart and does not coordinate across multiple server instances/workers. That's a real constraint of the current single-container deployment, not an oversight.

**Bugs found and fixed during verification (a real debugging trail, not a clean first try):**
1. Gemini client pointed at `gemini-flash-latest`, an experimental alias with restrictive rate limits — not suitable as a production fallback.
2. Switched to `gemini-2.0-flash` — didn't exist for this API key/project.
3. Switched to `gemini-2.5-flash` — deprecated for new API keys, per Google's own API error message.
4. Switched to `gemini-3.6-flash` — the model Google's own error message explicitly recommended. Confirmed working via direct API call.

**Confirmed after redeploy:** two full benchmark runs post-fix showed **zero application-level 500 crashes**, including on the exact question that failed 100% of the time before the fix.

**A genuine trade-off surfaced by the fix, not hidden:** the old (broken) behavior failed *fast* — an immediate 500 with no fallback attempted. The new behavior tries harder (Groq → backoff → Gemini → possibly multiple critic retries), which is more likely to eventually succeed but can occasionally push worst-case latency past what a client-side timeout expects. Two requests in one run hit a 90-second client timeout without an application error — meaning the system was still working, just slower than the benchmark's patience. This is a real, stated reliability-vs-latency trade-off, not resolved, just documented honestly.

## 4. A separate, still-open reliability issue: Azure infrastructure timeouts

One benchmark run hit a `ConnectTimeout` (couldn't even establish a TCP connection within 180s) — this is unrelated to the LLM fallback work. It points to Azure App Service itself briefly unreachable, most likely due to the hosting tier scaling down or idling after inactivity. This is a distinct, unresolved issue (App Service "Always On" setting / tier choice), not something the `local_llm.py` fix touches.

## 5. Quality vs. latency trade-off (real, observed)

The critic retry loop is a real, measured trade-off: when the critic scores an answer below 0.7, the agent redoes SQL generation, execution, reasoning, recommendation, and re-critiques — roughly **doubling the latency** for that question (observed: ~30s for a single pass vs. ~62s total when a retry fired) in exchange for catching and correcting a genuinely wrong/empty answer before it reaches the user. This is a deliberate, working trade — slower but more reliable — verified directly in production logs, not assumed.

## 6. Not yet done, stated plainly (no fabrication)

- **RAM usage**: measured via Azure's "Memory working set" metric (real, Azure-reported container memory, not an estimate):
  - 24-hour average: **162.8MB**
  - 7-day average: **209.5MB**
  - Peak immediately after a deploy/restart: **~700–800MB** (likely ONNX model + ChromaDB loading into memory on startup)
  - Idle troughs: **near 0–200MB** between activity bursts — consistent with the Free tier idle-unloading the container between requests, which also matches the UptimeRobot findings above.
  - Note: this is a still a short observation window dominated by an unusually high number of redeploys during active debugging (visible as the repeated spike pattern in the 7-day chart) — not a clean "normal operation" baseline. A longer, quieter observation period would give a more representative steady-state number.
- **Statistically robust latency benchmark**: current numbers are from single-digit sample sizes. A proper benchmark would need dozens of runs per question across different times of day.
- **Human-in-the-Loop (HITL) pipeline**: does not exist in this codebase. Not started.
- **Root cause of slow Neon SQL execution**: identified as a bottleneck, not yet investigated further.
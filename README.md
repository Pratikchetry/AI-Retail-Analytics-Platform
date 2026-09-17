# 🛍️ Retail Revenue Intelligence Platform

**An end-to-end, multi-agent AI copilot that answers natural-language questions about a UK retail business — reasoning over a live PostgreSQL warehouse, forecasting revenue with XGBoost, verifying its own answers against ground-truth data, and escalating what it isn't confident about to a human.**

> Every claim, number, and diagram in this README was independently verified during development — live HTTP checks against the deployed API, direct database queries against production, clean `--no-cache` Docker builds compared side by side, and a real, end-to-end tested Human-in-the-Loop pipeline. Where something wasn't verified, it's labeled as such rather than assumed.

---

## 📖 The Scenario This Was Built For

It's 4 PM. A finance team gets an email: tomorrow morning, the CFO is meeting the sales team and a major client, and needs to walk through last quarter's revenue, flag any anomalies, and show where the business stands.

Normally, that's a scramble — pull the data, write the SQL, build a dashboard, sanity-check the numbers, format it into slides. Two to five hours of work, minimum, the night before a meeting that was supposed to be routine.

Instead, someone shares a link. The finance team opens it, types a question — *"What was the total revenue last month?"* — and gets a real, data-backed answer in seconds. No dashboard to build. No queries to write by hand. They ask a follow-up — *"Which customer segment drove that?"* — and get another grounded answer, with the SQL and evidence behind it if anyone wants to check.

That's the product this repository builds: a chat interface in front of a real multi-agent system that queries a live warehouse, forecasts what's coming, catches anomalies, and — critically — knows when it isn't sure and flags that instead of guessing confidently.

---

## 🌐 Live Demo

| | |
|---|---|
| **Chat UI** | [ai-retail-analytics-platform.vercel.app](https://ai-retail-analytics-platform.vercel.app) — Next.js frontend on Vercel |
| **API** | FastAPI backend, containerized, deployed on Azure App Service |
| **Database** | PostgreSQL on [Neon](https://neon.tech) — serverless, verified in production |

> Hosted on free/low tiers for this portfolio project — see the **Honest Limitations** and **Reliability Findings** sections below for what that means in practice, measured, not assumed.

---

## 🏗️ Architecture — How a Question Actually Travels Through This System

```text
 Browser (Next.js, Vercel)
       |
       |  POST /ask  { "question": "..." }
       v
 FastAPI (Azure App Service, Docker container)
       |
       |  cache check (10-min TTL, MD5 of question)
       |  --- cache miss ---
       v
+-------------+
|   ROUTER    |  LLM call: is this SQL? Forecast? Anomaly? Out of scope?
+------+------+
       |
   +---+----+---------------+--------------+
   |        |               |              |
   v        v               v              v
SQL Chain  Forecast Node  Anomaly Node   Decline
   |       (XGBoost)     (Isolation      (out of
   |                       Forest)        scope)
   v
+---------------+
| RAG RETRIEVE  |  ChromaDB + local ONNX embedder → pull relevant
+-------+-------+  knowledge assets (schema docs, business rules, findings)
        v
+---------------+
|  COMPRESSOR   |  Keep top 3 chunks, drop the rest (real measured
+-------+-------+  reduction: ~67–76% of retrieved context, avg ~70%)
        v
+---------------+      +-----------+
|  SQL GENERATE |----->| VALIDATE  |--(fail)--> retry (max 3)
+-------+-------+      +-----+-----+
        |                    |(pass)
        v                    v
+---------------+      +-----------+
|  SQL EXECUTE  |----->| REASONING |  SQL result = ground truth
+---------------+      +-----+-----+  (Neon PostgreSQL)
                             v
                     +---------------+
                     |   VERIFIER    |  Cross-checks factual claims
                     | (warehouse    |  against the live warehouse —
                     |   wins)       |  warehouse wins on any conflict
                     +-------+-------+
                             v
                     +---------------+
                     |RECOMMENDATION |  "So what should we do about it"
                     +-------+-------+
                             v
                     +---------------+
                     |    CRITIC     |  Scores the final answer 0.0–1.0
                     | (retry <0.7)  |  Retries the whole chain if it fails
                     +-------+-------+
                             |
                  passes ----+---- still fails after 3 attempts
                     |                        |
                     v                        v
                 YOUR ANSWER          +altogether+
                                       | HITL QUEUE |  Logged to Neon for
                                       | (Neon)     |  human review — never
                                       +------------+  silently returned as
                                                        if it were confident
```
---
## 🏗️ Architecture — Diagram


<img width="4983" height="6420" alt="diagram (1)" src="https://github.com/user-attachments/assets/a1bc19bf-f4eb-4d0c-a988-83c0a853ea55" />


---

**LLM layer, and the resilience actually built into it:**

```text
Every LLM call in the graph above routes through:

  LocalLLM.generate(prompt)
        |
        v
  Groq (openai/gpt-oss-120b)  --- fails? --->  Gemini (gemini-3.6-flash)
        |                                            |
        v                                            v
   3 consecutive failures?                      also fails?
        |                                            |
        v                                            v
  Circuit breaker OPENS                    RuntimeError raised
  (skip Groq for 60s,                      with BOTH providers'
   go straight to Gemini)                  errors, for debugging
```

This fallback and circuit breaker did not exist for most of this project's development — see **"The Fallback That Wasn't"** below for the real debugging story behind it.

---

## 🧰 Tech Stack

![Python](https://img.shields.io/badge/Python-3.11-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-orange)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-blue)
![XGBoost](https://img.shields.io/badge/XGBoost-Forecasting-red)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![NextJS](https://img.shields.io/badge/Next.js-Frontend-black)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-black)
![Azure](https://img.shields.io/badge/Azure-App_Service-blue)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![MLflow](https://img.shields.io/badge/MLflow-MLOps-pink)

**LLM layer:** Groq (`openai/gpt-oss-120b`) primary, Google Gemini (`gemini-3.6-flash`) fallback, via a custom `LocalLLM` router with an in-process circuit breaker.
**Vector store:** ChromaDB + local ONNX Runtime inference (`all-MiniLM-L6-v2`) — no PyTorch dependency in production.
**Forecasting:** XGBoost V2 (MAE £6,892, R² 0.67, 67% better than naive baseline).
**Anomaly detection:** Isolation Forest (scikit-learn) — 144 anomalies flagged, 4.98% of country-days.
**Frontend:** Next.js (App Router), Tailwind CSS, Framer Motion — streams responses token-by-token via `ReadableStream`.
**Human-in-the-Loop:** answers that exhaust the critic's retry budget are logged to a dedicated Neon table (`human_review_queue`), reviewable and resolvable via `/review/pending` and `/review/{id}/resolve`.

---

## 📊 Ground Truth (Verified Against the Live Warehouse)

| Metric | Value |
|---|---|
| Total Revenue (all time) | **£20,476,634** |
| Fact Sales Rows | **1,007,914** |
| Best Month | November 2011 (£1,503,867) |
| True Superstar Product | **WHITE HANGING HEART T-LIGHT HOLDER** (£261,169, rank #1 on revenue, quantity, and orders) |
| Forecast Model (XGBoost V2) | **MAE £6,892 · R² 0.67 · 67% better than naive baseline** |
| Anomalies Detected | **144** (4.98% of country-days) |
| Context Compression | **~67–76% of retrieved context dropped** (measured across real production log traces) |

### The Bug the System Caught in Itself

Early in this project, the knowledge base confidently stated the top product was **"CREAM HANGING HEART T-LIGHT HOLDER."** The real answer, verified against the warehouse, is **"WHITE HANGING HEART T-LIGHT HOLDER."** The name had been wrong from the start — nobody caught it because nothing before this system's verifier step cross-checked documents against live data. The metadata verifier node caught the contradiction, corrected the answer, and the critic scored it 1.0. That's the entire reason the "warehouse wins on conflict" rule exists in the architecture above — it isn't theoretical, it's a fix for a bug this exact system found in its own knowledge base.

---

## 🐳 Docker Image Optimization — 14.4GB → 2.75GB

The embedding pipeline went through several real iterations while chasing memory constraints on a resource-limited deployment: local `sentence-transformers` (PyTorch-backed) → Gemini embedding API → HuggingFace Inference API → local ONNX Runtime. Each swap was a response to a real production failure (OOM, DNS blocks, API throttling), not a planned optimization roadmap.

Measured by building both the "before" (`sentence-transformers` + `torch`) and "after" (ONNX Runtime) versions from actual git history with `docker build --no-cache`, so both numbers are real and comparable:

| | Total Image Size | Unique Layers Added |
|---|---|---|
| Before (sentence-transformers + torch) | 14.4GB | 4.58GB |
| After (local ONNX Runtime) | **2.75GB** | **645MB** |

The production image (647MB) matches the "after" unique-layer measurement almost exactly, confirming the deployed service genuinely runs the ONNX path, not a stale build.

---

## 🔌 The Fallback That Wasn't (A Real Debugging Story)

The README used to claim: *"LLM Router: Gemini primary + Groq fallback."* That claim was false. `LocalLLM` only ever called Groq. `GeminiClient` existed in the codebase, fully written, and was never imported by anything. When Groq rate-limited (which it does, reliably, on the free tier under load), the entire agent request crashed with a raw `500`.

This was caught during a live benchmarking session, not a code review — a RAGAS evaluation run hit Groq's 429 and the whole pipeline died mid-question. Fixing it took four real attempts:

1. Wired `GeminiClient` into `LocalLLM` as an actual fallback, with a circuit breaker (3 consecutive Groq failures → skip Groq entirely for 60s, go straight to Gemini).
2. First model tried: `gemini-flash-latest` — technically valid, but Google's own docs flag it as experimental with restrictive rate limits. Failed under the same load that broke Groq.
3. Second attempt: `gemini-2.0-flash` — not available for this API key/project. `404`.
4. Third attempt: `gemini-2.5-flash` — deprecated for new API keys, per Google's own API error message, which explicitly named the replacement.
5. Fourth attempt, the one that worked: **`gemini-3.6-flash`** — confirmed via a standalone test, then verified in production logs after redeploy.

Post-fix, two full benchmark runs against production showed **zero application-level 500 crashes**, including on the exact question that had failed 100% of the time before the fix. Full detail, including the real trade-off this surfaced (the system now tries harder and occasionally takes longer, rather than failing fast) is in [`docs/reliability.md`](docs/reliability.md).

---

## 🚨 The "6-Day Outage" That Wasn't

UptimeRobot reported this API as "Down" continuously for over 6 days. The API was never actually down — every real request during that window succeeded. The root cause: UptimeRobot's monitor was configured to send `HEAD` requests, and the FastAPI `/health` route was defined with `@app.get("/health")`, which doesn't handle `HEAD` by default. Every monitoring check got a `405 Method Not Allowed` and was correctly interpreted as "down," even though the actual API was healthy the entire time.

Fixed by changing the route to `@app.api_route("/health", methods=["GET", "HEAD"])` (and the same for `/`). Confirmed resolved: UptimeRobot flipped to "Up" within minutes of the fix deploying.

---

## 🧪 RAGAS Evaluation (Real Scores, Real Caveats)

`tests/eval_ragas.py` runs the actual LangGraph agent against 5 golden-dataset questions and scores the results with RAGAS's context precision, context recall, and faithfulness metrics, using Groq as the judge LLM.

| Metric | Score |
|---|---|
| Context Precision | 0.60 |
| Context Recall | 0.40 |
| Faithfulness | 0.38 |

**Stated honestly:** this run completed successfully, but a later re-run (after fixing a ground-truth error in the test file itself — it had inherited the same "CREAM" typo the verifier catches at runtime) crashed partway through due to Groq rate-limiting, before the Gemini fallback existed. These numbers are from one completed run with a different underlying model than is currently in production for some nodes, and should be read as a first measurement, not a stable benchmark. A properly repeated run, post-fallback-fix, would be needed to trust these numbers as representative.

---

## 🙋 Human-in-the-Loop — Built, Tested, Deployed

When the critic node exhausts its retry budget (3 attempts) and still scores an answer below 0.7, the old behavior was to return that weak answer to the user with no indication it was low-confidence. Now, it's logged instead:

```
POST /ask (internally) → critic fails 3x → flag_for_review() →
  INSERT INTO human_review_queue (question, answer, critic_score, ...)
```

- `GET /review/pending` — lists flagged answers, most recent first
- `POST /review/{id}/resolve` — mark reviewed, add notes, optionally supply a corrected answer

This was tested end-to-end before deployment: a fake low-confidence result was inserted directly, confirmed retrievable via the Python module, then confirmed retrievable and resolvable via the actual live HTTP API, then confirmed working against the production Neon database after deploy (`curl .../review/pending` returns real, correct data).

---

## 📈 Reliability & Latency — Measured, Not Assumed

Full detail in [`docs/reliability.md`](docs/reliability.md). Headline numbers:

| Metric | Value | Caveat |
|---|---|---|
| Full pipeline latency (p50) | ~18–37s across runs | Small sample size (n=3–5 per run) |
| Cached response latency (p50) | ~0.9–1.7s | ~10–20x faster than a fresh run |
| RAM usage (Azure "Memory working set") | 162.8MB (24h avg) / 209.5MB (7-day avg) | Peaks ~700–800MB right after a deploy/restart |
| Docker image size | 2.75GB (from 14.4GB) | Verified via clean `--no-cache` builds |
| Largest single latency cost | Groq 429 backoff, up to ~30s per occurrence | Direct consequence of the free tier under load |

---

## 🚀 Quickstart

### Option A: Docker (recommended)

```bash
docker compose -f docker/docker-compose.yml up --build setup
docker compose -f docker/docker-compose.yml up -d
```

- **Chat UI:** http://localhost:8001
- **API Docs (Swagger):** http://localhost:8000/docs

### Option B: Local Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add GROQ_API_KEY, GEMINI_API_KEY, DATABASE_URL

PYTHONPATH=. python -m src.pipeline all
./run_app.sh
```

> `DATABASE_URL` points to Neon in production; local development uses a Docker-provisioned Postgres instance instead.

---

## 🔌 API Endpoints

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/ask` | Natural language → full agent response |
| `POST` | `/chat` | Streaming variant for the Next.js frontend |
| `POST` | `/forecast` | Direct XGBoost model access |
| `POST` | `/ingest` | Reload warehouse from staging CSVs |
| `GET`/`HEAD` | `/` | Root health check (Azure) |
| `GET`/`HEAD` | `/health` | Service + dependency health check |
| `GET` | `/metrics` | KPI snapshot |
| `GET` | `/custom/monthly-revenue` | Monthly revenue time series |
| `GET` | `/custom/segment-revenue` | Customer segment breakdown |
| `GET` | `/review/pending` | List answers flagged for human review |
| `POST` | `/review/{id}/resolve` | Resolve a flagged answer |

---

## 🎓 Honest Limitations

- **Groq free tier** throttles under load — mitigated by the Gemini fallback and circuit breaker, but not eliminated; the trade-off is documented in `reliability.md`, not hidden.
- **Azure Free tier** has a hard daily CPU quota and idles the container between requests — RAM troughs near 0MB in the metrics reflect this.
- **RAGAS scores** are a single, unrepeated measurement — stated plainly above, not smoothed over.
- **SQL execution against Neon** occasionally takes 4.7–7s for simple queries — flagged as an open, unsolved bottleneck.
- **No distributed circuit breaker** — the Groq/Gemini breaker is per-process; a multi-instance deployment would need shared state (e.g., Redis) for the same protection.

---

## 📄 License

MIT

---

> *Built from scratch, debugged in production, and documented honestly — including the bugs that were found and the ones that are still open.*

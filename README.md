# 🛍️ Retail Revenue Intelligence Platform

**An end-to-end, multi-agent AI copilot that answers natural-language questions about a UK retail business — reasoning over a live PostgreSQL warehouse, forecasting revenue with XGBoost, and verifying its own answers against ground-truth data.**

> Not a tutorial project. Not a demo with hardcoded answers. Every metric below traces to real warehouse data or a real trained model.

---

## 🎯 Why This Project Is Different

| | |
|---|---|
| **1.2M+ rows** of real UK retail transactions processed through a custom ETL pipeline | **12-node LangGraph agent** with routing, context compression, self-verification, and a critic quality gate |
| **MAE £6,892** XGBoost forecast model (67% better than baseline) — tracked in MLflow | **The agent caught its own data bug**: a knowledge-base claim was wrong, the verifier flagged it, and the warehouse truth won |
| **77% prompt noise reduction** via context engineering (not just RAG) | **One-command Docker bootstrap** — schema, data, models, embeddings, API, UI |

---

## 🧰 Tech Stack

![Python](https://img.shields.io/badge/Python-3.11-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-orange)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Warehouse-blue)
![XGBoost](https://img.shields.io/badge/XGBoost-Forecasting-red)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Chainlit](https://img.shields.io/badge/Chainlit-UI-purple)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![MLflow](https://img.shields.io/badge/MLflow-MLOps-pink)
![GitHub Actions](https://img.shields.io/badge/CI/CD-GitHub_Actions-black)

**LLM Layer:** Google Gemini 2.0 Flash (primary) + Groq llama-3.3-70b (fallback) via a custom LLM Router
**Vector Store:** ChromaDB + sentence-transformers (all-MiniLM-L6-v2)
**Anomaly Detection:** Isolation Forest (scikit-learn)

---

## 📖 The Story (What This Actually Does)

You're the CEO of a UK gift retailer. You open a chat window and type:

> *"Why did revenue drop last quarter, and what should I do about it?"*

A traditional dashboard can't answer that. This system can. Here's what happens in the ~8 seconds before you get a response:

1. **A router agent classifies your intent** — Is this a SQL lookup? A forecast request? Out of scope (like asking about TikTok ad spend)? It decides before touching the database.
2. **A RAG retriever pulls relevant context** from 174 business knowledge assets (schema docs, business rules, findings) — then a **context compressor throws away 77% of it**, keeping only the 3 most relevant chunks. Less noise = fewer hallucinations.
3. **A SQL agent writes real PostgreSQL**, a validator checks it against 7 business rules (no `SELECT *`, never join accounting adjustments unless asked, etc.), and it executes against the live warehouse.
4. **A reasoning agent synthesizes the answer** using an evidence hierarchy: SQL result is ground truth; knowledge base is supporting context only.
5. **A metadata verifier cross-checks factual claims against the warehouse.** If the knowledge base says "Product X is the superstar" but the data disagrees, **the warehouse wins** and the answer is corrected automatically.
6. **A critic scores the final answer 0.0–1.0.** If it's below 0.7, the agent retries. You never see a low-quality answer.

### The Moment That Made This Project Real

During testing, the agent was asked: *"What is the only true Superstar product?"*

The knowledge base confidently said **"CREAM HANGING HEART T-LIGHT HOLDER."**

The verifier queried the warehouse. The real top product was **WHITE HANGING HEART T-LIGHT HOLDER** (£261,169, rank #1 on all three dimensions). The name "CREAM" had been wrong since day one — baked into the project docs by mistake. Nobody noticed because every system before this one trusted the documents blindly.

This system didn't. The verifier flagged the conflict, corrected the answer, and the critic passed it at 1.0.

**That's what context engineering means.** Not just retrieving documents — deciding what to trust.

---

## 🏗️ Architecture (Plain English)

```text
You type a question
       |
       v
+-------------+
|   ROUTER    |  "Is this SQL? Forecast? Out of scope?"
+------+------+
       |
   +---+----+---------------+--------------+
   |        |               |              |
   v        v               v              v
SQL Chain  Forecast Node  Anomaly Node   Decline
   |       (XGBoost)    (Isolation      (out of
   |                      Forest)        scope)
   v
+---------------+
| RAG RETRIEVE  |  Pull 174 knowledge assets
+-------+-------+
        v
+---------------+
|  COMPRESSOR   |  Keep top 3, drop 77% noise
+-------+-------+
        v
+---------------+      +-----------+
|  SQL GENERATE |---> | VALIDATE  |--(fail)--> retry (max 3)
+-------+-------+      +-----+-----+
        |                    |(pass)
        v                    v
+---------------+      +-----------+
|  SQL EXECUTE  |---> | REASONING |  (SQL = ground truth)
+---------------+      +-----+-----+
                             v
                     +---------------+
                     |   VERIFIER    |  Cross-check claims vs warehouse
                     | (warehouse    |  (warehouse wins on conflict)
                     |   wins)       |
                     +-------+-------+
                             v
                     +---------------+
                     |RECOMMENDATION |  "So what / do this"
                     +-------+-------+
                             v
                     +---------------+
                     |    CRITIC     |  Score 0.0-1.0
                     | (block < 0.7) |  (retry if low)
                     +-------+-------+
                             v
                         YOUR ANSWER
```

**Why this design (not just "a RAG chatbot"):**
- **Agents vs. Nodes:** Business logic (SQL generation, validation) lives in reusable `src/agent/` classes. Control flow (routing, retries, critic loops) lives in `src/langgraph/nodes/`. You don't ask the SQL specialist to also manage the company — same principle.
- **Context engineering > pure RAG:** RAG retrieves everything. Context engineering decides what *survives* (compressor), what *gets trusted* (verifier), and what *wins* on conflict (warehouse). This is why the system has a 100% pass rate on scored eval questions.
- **No Airflow:** For a single pipeline, Airflow is overhead. The `src.pipeline` CLI + Docker handles orchestration with retry logic already built into LangGraph.

---

## 📊 Ground Truth (Verified Numbers)

Every number here comes from the live warehouse or a real model artifact — not estimates.

| Metric | Value |
|---|---|
| Total Revenue (all time) | **£20,476,634** |
| Fact Sales Rows | **1,007,914** |
| Customers / Products / Countries | 5,879 / 4,917 / 43 |
| Best Month | November 2011 (£1,503,867) |
| YoY Growth | −0.13% (Dec 2011 partial-month artifact, not real decline) |
| True Superstar Product | **WHITE HANGING HEART T-LIGHT HOLDER** (£261,169, rank #1 on revenue + quantity + orders) |
| Forecast Model (XGBoost V2) | **MAE £6,892 · R² 0.67 · 67% better than naive baseline** |
| Anomalies Detected | **144** (4.98% of country-days, including the famous Dec 9 £196K spike) |
| 30-Day Forecast Total | £2,195,974 (avg £73,199/day) |
| LLM Calls Per Question | **5** (optimized down from 9 via graph deduplication) |
| Context Noise Reduction | **77%** (via context compressor) |
| Eval Pass Rate | **5/5 = 100%** on scored questions |

---

## 🚀 Quickstart

### Option A: Docker (one command — recommended)

```bash
# 1. Bootstrap the full stack (schema + 1M rows + models + embeddings)
docker compose -f docker/docker-compose.yml up --build setup

# 2. Start the product (API + UI + Postgres)
docker compose -f docker/docker-compose.yml up -d
```

Then open:
- **Chat UI:** http://localhost:8001
- **API Docs (Swagger):** http://localhost:8000/docs

### Option B: Local Development

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add GROQ_API_KEY and GEMINI_API_KEY

# Run the full data + ML pipeline
PYTHONPATH=. python -m src.pipeline all

# Start API + UI together
./run_app.sh
```

---

## 🔌 API Endpoints

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/ask` | Natural language → full agent response (answer, SQL, evidence, critic score) |
| `POST` | `/forecast` | Direct XGBoost model access (bypass router) |
| `POST` | `/ingest` | Reload warehouse from staging CSVs |
| `GET` | `/health` | Service + dependency health check |
| `GET` | `/metrics` | KPI snapshot from the warehouse |
| `GET` | `/custom/monthly-revenue` | Monthly revenue time series (chart data) |
| `GET` | `/custom/segment-revenue` | Customer segment breakdown |

---

## 🗂️ Project Structure

```
retail-revenue-intelligence/
├── src/
│   ├── agent/              # Reusable capabilities (SQL gen, validation, reasoning)
│   ├── langgraph/          # The multi-agent brain (StateGraph + 12 nodes)
│   ├── ml/                 # Real ML models (XGBoost V2, Isolation Forest)
│   ├── ingestion/          # CSV → warehouse ETL (real, not mock)
│   ├── rag/                # ChromaDB + hybrid keyword/semantic retrieval
│   ├── app/                # FastAPI backend + Chainlit UI
│   ├── executor/           # Read-only warehouse executor (pooled)
│   ├── llm/                # LLM Router (Gemini 2.0 + Groq fallback)
│   └── utils/              # Config, DB engine, logger
├── sql/                    # Schema, seeds, 15 analytics views, feature tables
├── assets/                 # 24 schema YAMLs, 13 metric defs, 7 business rules
├── knowledge_base/         # Markdown findings (the RAG knowledge layer)
├── docker/                 # Dockerfile + docker-compose (app + postgres)
├── tests/                  # Router test, eval harness, integration tests
├── .github/workflows/      # CI: lint + import validation + router test
└── requirements.txt
```

---

## 🧪 Quality & Engineering Decisions

### Context Engineering (the differentiator)
Most RAG systems dump retrieved documents into a prompt and hope. This system enforces a trust hierarchy:
- **Layer 1 — Routing:** Out-of-scope questions (TikTok, competitors) rejected before touching the warehouse.
- **Layer 2 — Compression:** Top-3 relevant chunks only; 77% noise dropped.
- **Layer 3 — Evidence Hierarchy:** SQL result = ground truth. Knowledge base = context only.
- **Layer 4 — Verification:** Factual claims cross-checked against live data. Warehouse wins on conflict.
- **Layer 5 — Critique:** Final answer scored 0.0–1.0. Below 0.7 = retry.

### MLOps
- XGBoost training logs parameters, metrics (MAE, RMSE, R², baseline comparison), and model artifacts to **MLflow Tracking**.
- Model registered in **MLflow Model Registry** with versioning.
- Local `.pkl` artifact also saved for the LangGraph forecast node to load at inference time.

### CI/CD
- GitHub Actions runs on every PR/push: Ruff lint → import validation → router unit test.
- Router test uses GitHub Secrets for the Groq API key; fails gracefully (non-blocking) if secret missing.

### Honest Limitations
- **Groq free tier** throttles rapid bursts; mitigated by LLM Router (Gemini primary, Groq fallback) + exponential backoff.
- **Forecast model** underpredicts rare extreme spike days (like Dec 9) — documented honestly in the metrics JSON, not hidden.
- **ChromaDB** has no partitioning (174 assets = brute-force search is instant; partitioning would add complexity for zero gain at this scale).

---

## 🎓 What I Learned 

**Q: Why LangGraph instead of a simple chain?**
A chain is linear. This system needs conditional branching (route by intent), retry loops (validation failure, critic failure), and parallel tool dispatch (SQL vs forecast vs anomaly). LangGraph's StateGraph expresses that control flow cleanly. A chain would force it into spaghetti.

**Q: Why separate `src/agent/` and `src/langgraph/nodes/`?**
Agents contain business logic (the SQL prompt, the validation rules). Nodes contain control flow (when to retry, what state to write). Separating them means I can unit-test "does this SQL agent generate valid SQL?" without spinning up the whole graph. Same pattern as LangChain tools + agent loop.

**Q: What's context engineering and why does it matter?**
RAG retrieves everything. Context engineering decides what survives (compressor), what gets trusted (verifier), and what wins on conflict (warehouse). It's the difference between a system that hallucinates confidently and one that caught its own data bug.

**Q: Why no Airflow?**
For a single pipeline, Airflow is overhead. My `src.pipeline` CLI handles orchestration with retries already built into LangGraph. Airflow shines when you have dozens of pipelines across teams — not here.

---

## 📄 License

MIT

---

> *Built from scratch — real data, real models, real architecture decisions. No tutorial copies, no hardcoded answers.*

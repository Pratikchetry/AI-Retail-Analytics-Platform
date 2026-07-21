"""
Phase 3 — AI Retail Intelligence Platform
FastAPI service layer.

Exposes the LangGraph agent brain + models as a clean REST API:
  POST /ask       — natural language question -> full agent response
  POST /forecast  — direct model forecast (bypass router)
  POST /ingest    — re-run ingestion (CSV -> warehouse)
  GET  /health    — service + dependency health
  GET  /metrics   — KPI snapshot from the warehouse

Run: uvicorn src.app.api:app --reload --port 8000
"""

import os
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
import pandas as pd

from src.utils.db import engine
from src.utils.logger import get_logger
from src.app.schemas import (
    AskRequest, AskResponse,
    ForecastRequest, ForecastResponse,
    IngestRequest, IngestResponse,
    HealthResponse, MetricsResponse,
)

log = get_logger(__name__)

app = FastAPI(
    title="Retail Revenue Intelligence API",
    description="Multi-agent analytics copilot for UK retail revenue data.",
    version="1.0.0",
)

# Allow the Streamlit UI (Phase 4) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------------------------
# POST /ask — the main endpoint
# ------------------------------------------------------------------
@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    """Ask the multi-agent system a natural language question."""
    log.info("API /ask: '%s'", req.question[:80])
    try:
        from src.langgraph.graph import run_agent
        result = run_agent(req.question)
        return AskResponse(
            question=req.question,
            route=result.get("route", ""),
            answer=result.get("answer", ""),
            recommendation=result.get("recommendation", ""),
            evidence=result.get("evidence", ""),
            critic_score=result.get("critic_score", 0.0),
            critic_passes=result.get("critic_passes", False),
            sql=result.get("sql"),
            execution_status=result.get("execution_status"),
            result_data=result.get("result_data"),
        )
    except Exception as e:
        log.error("/ask failed: %s", str(e)[:300])
        raise HTTPException(status_code=500, detail=str(e)[:300])


# ------------------------------------------------------------------
# POST /forecast — direct model access (no router)
# ------------------------------------------------------------------
@app.post("/forecast", response_model=ForecastResponse)
def forecast(req: ForecastRequest):
    """Generate a model-backed revenue forecast."""
    log.info("API /forecast: horizon=%d", req.horizon)
    try:
        from src.ml.generate_forecast import generate_forecast
        from src.utils.db import engine as eng

        forecasts = generate_forecast(horizon=req.horizon)

        # Persist to warehouse
        from src.ml.generate_forecast import save_forecast
        save_forecast(forecasts)

        total = sum(f["forecast_revenue"] for f in forecasts)

        # Load model accuracy
        mae = None
        if os.path.exists("outputs/reports/forecast_summary_xgboost.json"):
            with open("outputs/reports/forecast_summary_xgboost.json") as f:
                mae = json.load(f).get("mae")

        return ForecastResponse(
            horizon=req.horizon,
            total_revenue=round(total, 2),
            avg_daily_revenue=round(total / len(forecasts), 2),
            days=forecasts,
            model_name="XGBoost_V2",
            model_mae=mae,
        )
    except Exception as e:
        log.error("/forecast failed: %s", str(e)[:300])
        endpoint_detail = "Model not trained. Run: python -m src.ml.train_xgboost_v2"
        raise HTTPException(status_code=500, detail=endpoint_detail if "not found" in str(e).lower() else str(e)[:300])


# ------------------------------------------------------------------
# POST /ingest — re-run ingestion
# ------------------------------------------------------------------
@app.post("/ingest", response_model=IngestResponse)
def ingest(req: IngestRequest):
    """Trigger warehouse re-ingestion from staging CSVs."""
    log.info("API /ingest: %s", req.csv_name)
    try:
        from src.ingestion.load_warehouse import run_full_ingestion, ANALYTICS_PIPELINE
        run_full_ingestion()
        rows = 0
        with engine.connect() as conn:
            rows = conn.execute(text("SELECT COUNT(*) FROM fact_sales")).scalar()
        return IngestResponse(
            status="complete",
            rows_loaded=rows,
            analytics_tables_rebuilt=len(ANALYTICS_PIPELINE),
        )
    except Exception as e:
        log.error("/ingest failed: %s", str(e)[:300])
        raise HTTPException(status_code=500, detail=str(e)[:300])


# ------------------------------------------------------------------
# GET /health
# ------------------------------------------------------------------
@app.get("/health", response_model=HealthResponse)
def health():
    """Service + dependency health check."""
    db_status = "disconnected"
    model_loaded = os.path.exists("src/ml/models/forecast_xgb_v2.pkl")
    chroma_assets = None

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            db_status = "connected"
            fact_count = conn.execute(text("SELECT COUNT(*) FROM fact_sales")).scalar()
            db_status = f"connected ({fact_count:,} fact_sales rows)"
    except Exception as e:
        log.warning("Health check DB error: %s", str(e)[:100])

    return HealthResponse(
        status="healthy",
        database=db_status,
        model_loaded=model_loaded,
        chroma_assets=chroma_assets,
    )


# ------------------------------------------------------------------
# GET /metrics — KPI snapshot
# ------------------------------------------------------------------
@app.get("/metrics", response_model=MetricsResponse)
def metrics():
    """Business KPI snapshot from the warehouse."""
    try:
        with engine.connect() as conn:
            exec_row = conn.execute(text(
                "SELECT total_revenue, best_month, best_month_revenue, yoy_growth "
                "FROM revenue_executive_summary LIMIT 1"
            )).fetchone()

            total_orders = conn.execute(text(
                "SELECT COUNT(DISTINCT invoice) FROM fact_sales"
            )).scalar()

            anomalies = conn.execute(text(
                "SELECT COUNT(*) FROM ml_anomaly_scores WHERE is_anomaly = TRUE"
            )).scalar()

        mae = None
        if os.path.exists("outputs/reports/forecast_summary_xgboost.json"):
            with open("outputs/reports/forecast_summary_xgboost.json") as f:
                mae = json.load(f).get("mae")

        return MetricsResponse(
            total_revenue=float(exec_row[0]) if exec_row else 0,
            total_orders=total_orders or 0,
            best_month=exec_row[1] if exec_row else "unknown",
            best_month_revenue=float(exec_row[2]) if exec_row else 0,
            yoy_growth=float(exec_row[3]) if exec_row and exec_row[3] is not None else None,
            forecast_model_mae=mae,
            anomalies_detected=anomalies or 0,
        )
    except Exception as e:
        log.error("/metrics failed: %s", str(e)[:300])
        raise HTTPException(status_code=500, detail=str(e)[:300])


@app.get("/custom/monthly-revenue")
def monthly_revenue():
    """Monthly revenue time series for the dashboard chart."""
    try:
        with engine.connect() as conn:
            df = pd.read_sql(text(
                "SELECT month_date, month_name || ' ' || year AS label, "
                "total_revenue, total_orders "
                "FROM revenue_monthly_summary ORDER BY month_date"
            ), conn)
        return df.to_dict(orient="records")
    except Exception as e:
        log.error("/custom/monthly-revenue failed: %s", str(e)[:300])
        raise HTTPException(status_code=500, detail=str(e)[:300])


@app.get("/custom/segment-revenue")
def segment_revenue():
    """Customer segment revenue breakdown for the dashboard."""
    try:
        with engine.connect() as conn:
            df = pd.read_sql(text(
                "SELECT customer_segment, customer_count, total_revenue, "
                "avg_order_revenue "
                "FROM customer_segment_revenue ORDER BY total_revenue DESC"
            ), conn)
        return df.to_dict(orient="records")
    except Exception as e:
        log.error("/custom/segment-revenue failed: %s", str(e)[:300])
        raise HTTPException(status_code=500, detail=str(e)[:300])

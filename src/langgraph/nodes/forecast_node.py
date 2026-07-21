"""
Phase 2 — AI Retail Intelligence Platform
Forecast Node.

Calls the real XGBoost V2 model to produce a revenue forecast.
Fast path: if fresh forecasts exist in the revenue_forecast table, use them.
Slow path: generate via src.ml.generate_forecast on the fly.
"""

import os
import json
from datetime import datetime, timedelta

import pandas as pd
from sqlalchemy import text

from src.utils.db import engine
from src.utils.logger import get_logger
from src.langgraph.state import AgentState

log = get_logger(__name__)

MODEL_PATH = "src/ml/models/forecast_xgb_v2.pkl"
METRICS_PATH = "outputs/reports/forecast_summary_xgboost.json"


def forecast_node(state: AgentState) -> dict:
    """Generate a model-backed revenue forecast and summarize it."""
    question = state["question"]
    log.info("Forecast node for: '%s'", question[:60])

    # ---- Parse horizon from the question (default 30) ----
    horizon = 30
    q_lower = question.lower()
    for n in (7, 14, 30, 60, 90):
        if str(n) in q_lower or ("week" in q_lower and n == 7):
            horizon = n
            break

    # ---- Fast path: use existing fresh forecasts if enough exist ----
    df_existing = None
    try:
        with engine.connect() as conn:
            df_existing = pd.read_sql(
                text(f"SELECT forecast_date, forecast_revenue FROM revenue_forecast "
                     f"ORDER BY forecast_date LIMIT {horizon}"), conn)
    except Exception as e:
        log.warning("Could not read existing forecasts: %s", e)

    if df_existing is not None and len(df_existing) >= horizon:
        log.info("Using %d existing forecasts from revenue_forecast table", horizon)
        forecast_rows = df_existing.to_dict(orient="records")
    else:
        # ---- Slow path: generate on the fly ----
        log.info("Generating fresh forecast (horizon=%d)", horizon)
        if not os.path.exists(MODEL_PATH):
            return _decline("Forecast model not trained. Run: python -m src.ml.train_xgboost_v2")
        try:
            from src.ml.generate_forecast import generate_forecast
            forecast_rows = generate_forecast(horizon=horizon)
        except Exception as e:
            log.error("Forecast generation failed: %s", e)
            return _decline(f"Forecast generation failed: {str(e)[:200]}")

    # ---- Build the answer ----
    total = sum(float(r["forecast_revenue"]) for r in forecast_rows)
    avg = total / len(forecast_rows)
    first_date = forecast_rows[0]["forecast_date"]
    last_date = forecast_rows[-1]["forecast_date"]

    # Load model accuracy for honest citation
    accuracy = ""
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH) as f:
            m = json.load(f)
        accuracy = (f"Model: XGBoost V2 | MAE £{m.get('mae', '?'):,.2f} | "
                    f"R² {m.get('r2', '?')}")

    answer = (
        f"Revenue forecast for the next {len(forecast_rows)} days "
        f"({first_date} to {last_date}):\n"
        f"- Total forecast revenue: £{total:,.2f}\n"
        f"- Average daily revenue: £{avg:,.2f}\n"
        f"- First day: £{float(forecast_rows[0]['forecast_revenue']):,.2f}\n"
        f"- Final day: £{float(forecast_rows[-1]['forecast_revenue']):,.2f}\n"
        f"\n{accuracy}"
    )

    # Compact row data for evidence
    evidence = "\n".join(
        f"  {r['forecast_date']}  £{float(r['forecast_revenue']):>12,.2f}"
        for r in forecast_rows[:10]
    )

    log.info("Forecast complete | %d days | total £%.2f | avg £%.2f",
             len(forecast_rows), total, avg)

    return {
        "rows": json.dumps(forecast_rows, default=str),
        "execution_status": "SUCCESS",
        "answer": answer,
        "evidence": evidence,
        "result_data": forecast_rows,
    }


def _decline(msg: str) -> dict:
    return {"answer": msg, "evidence": "", "execution_status": "SKIPPED"}
"""
Phase 0 — AI Retail Intelligence Platform
Unified pipeline CLI.

Runs the full data + ML stack from one entry point:
    python -m src.pipeline <command>

Commands:
    ingest     — Load staging CSVs -> warehouse + rebuild analytics/features
    train      — Train XGBoost V2 on real warehouse data
    score      — Run Isolation Forest anomaly detection on real data
    forecast   — Generate revenue forecast from trained model
    all        — Run everything in order (ingest -> train -> score -> forecast)
    status     — Print warehouse + model health summary
"""

import argparse
import os
import json

from sqlalchemy import text
from src.utils.db import engine
from src.utils.logger import get_logger

log = get_logger(__name__)


def cmd_ingest():
    from src.ingestion.load_warehouse import run_full_ingestion
    run_full_ingestion()


def cmd_train():
    from src.ml.train_xgboost_v2 import train_and_evaluate
    metrics = train_and_evaluate()
    log.info("Training complete | MAE £%.2f | R² %.4f", metrics["mae"], metrics["r2"])


def cmd_score():
    from src.ml.score_anomalies import score_anomalies
    metrics = score_anomalies()
    log.info("Anomaly scoring complete | %d anomalies (%.2f%%)",
             metrics["anomalies_detected"], metrics["anomaly_rate_pct"])


def cmd_forecast():
    from src.ml.generate_forecast import generate_forecast, save_forecast
    forecasts = generate_forecast(horizon=30)
    save_forecast(forecasts)


def cmd_all():
    log.info("=" * 60)
    log.info("RUNNING FULL PIPELINE (ingest -> train -> score -> forecast)")
    log.info("=" * 60)
    cmd_ingest()
    cmd_train()
    cmd_score()
    cmd_forecast()
    log.info("=" * 60)
    log.info("FULL PIPELINE COMPLETE")
    log.info("=" * 60)


def cmd_status():
    """Print a health summary of the warehouse + ML artifacts."""
    log.info("=" * 60)
    log.info("SYSTEM STATUS")
    log.info("=" * 60)

    # ---- Warehouse ----
    tables = [
        "fact_sales", "dim_product", "dim_customer", "dim_country", "dim_date",
        "revenue_monthly_summary", "revenue_growth_analysis", "yoy_revenue_analysis",
        "customer_segment_revenue", "product_performance_matrix",
        "feature_daily_model_input", "ml_anomaly_scores", "revenue_forecast",
    ]
    log.info("--- Warehouse ---")
    for t in tables:
        try:
            with engine.connect() as conn:
                n = conn.execute(text(f"SELECT COUNT(*) FROM {t}")).scalar()
            log.info("  %-34s %s rows", t, n)
        except Exception:
            log.warning("  %-34s MISSING", t)

    # ---- ML artifacts ----
    log.info("--- ML Artifacts ---")
    model_path = "src/ml/models/forecast_xgb_v2.pkl"
    log.info("  XGBoost V2 model: %s",
             "EXISTS" if os.path.exists(model_path) else "MISSING (run: train)")

    for report in ["outputs/reports/forecast_summary_xgboost.json",
                    "outputs/reports/anomaly_summary.json"]:
        if os.path.exists(report):
            with open(report) as f:
                data = json.load(f)
            if "mae" in data:
                log.info("  %s: MAE £%.2f, R² %.4f", report, data["mae"], data.get("r2", 0))
            elif "anomalies_detected" in data:
                log.info("  %s: %d anomalies", report, data["anomalies_detected"])
        else:
            log.warning("  %s: MISSING", report)


def main():
    parser = argparse.ArgumentParser(
        description="Retail Intelligence Pipeline CLI"
    )
    parser.add_argument(
        "command",
        choices=["ingest", "train", "score", "forecast", "all", "status"],
        help="Pipeline stage to run",
    )
    args = parser.parse_args()

    commands = {
        "ingest": cmd_ingest,
        "train": cmd_train,
        "score": cmd_score,
        "forecast": cmd_forecast,
        "all": cmd_all,
        "status": cmd_status,
    }
    commands[args.command]()


if __name__ == "__main__":
    main()
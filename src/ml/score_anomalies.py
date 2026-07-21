"""
Phase 0 — AI Retail Intelligence Platform
Real anomaly scoring pipeline.

Pulls real daily revenue from the warehouse, runs Isolation Forest,
and writes genuine scores into ml_anomaly_scores (replacing any mock data).
Reuses the existing RetailAnomalyEngine in src/ml/isolation_forest.py.
"""

import json
from datetime import datetime

import pandas as pd
from sqlalchemy import text

from src.utils.db import engine
from src.utils.logger import get_logger
from src.ml.isolation_forest import RetailAnomalyEngine

log = get_logger(__name__)

METRICS_PATH = "outputs/reports/anomaly_summary.json"

# Authoritative schema for ml_anomaly_scores.
# Recreated here so we are immune to any leftover mock table from seed_warehouse.py.
CREATE_TABLE_SQL = """
CREATE TABLE ml_anomaly_scores (
    order_date       DATE NOT NULL,
    country_name     TEXT,
    daily_revenue    NUMERIC(16,4) NOT NULL,
    daily_orders     INT NOT NULL,
    anomaly_score    NUMERIC(16,6) NOT NULL,
    is_anomaly       BOOLEAN NOT NULL,
    scored_at        TIMESTAMP DEFAULT NOW()
)
"""


def load_daily_revenue() -> pd.DataFrame:
    """Real daily revenue + order counts straight from fact_sales."""
    log.info("Loading daily revenue from fact_sales ...")
    sql = text("""
        SELECT
            fs.order_date,
            dc.country_name,
            SUM(fs.revenue) AS daily_revenue,
            COUNT(DISTINCT fs.invoice) AS daily_orders
        FROM fact_sales fs
        JOIN dim_country dc ON fs.country_key = dc.country_key
        GROUP BY fs.order_date, dc.country_name
        ORDER BY fs.order_date
    """)
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn)
    log.info("Loaded %d daily-country rows | dates %s -> %s",
             len(df), df["order_date"].min(), df["order_date"].max())
    return df


def score_anomalies():
    df = load_daily_revenue()
    if df.empty:
        raise RuntimeError("No daily revenue data found in fact_sales.")

    log.info("Running Isolation Forest (contamination=0.05) ...")
    engine_ml = RetailAnomalyEngine(contamination=0.05, random_state=42)
    scored = engine_ml.fit_predict_dataframe(df, revenue_col="daily_revenue")

    n_anomalies = int(scored["is_anomaly"].sum())
    log.info("Detected %d anomalies out of %d rows (%.2f%%)",
             n_anomalies, len(scored), (n_anomalies / len(scored)) * 100)

    # ---- Recreate ml_anomaly_scores with the correct schema ----
    log.info("Recreating ml_anomaly_scores with correct schema ...")
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS ml_anomaly_scores"))
        conn.execute(text(CREATE_TABLE_SQL))

    # ---- Write genuine scores ----
    log.info("Writing scores to ml_anomaly_scores ...")
    to_write = scored[[
        "order_date", "country_name", "daily_revenue", "daily_orders",
        "anomaly_score", "is_anomaly"
    ]].copy()
    to_write["scored_at"] = datetime.now()

    to_write.to_sql("ml_anomaly_scores", engine, if_exists="append", index=False)
    log.info("Wrote %d rows to ml_anomaly_scores", len(to_write))

    # ---- Persist honest metrics for the anomaly agent ----
    spike = scored[scored["is_anomaly"] & (scored["anomaly_direction"] == "spike")]
    drop = scored[scored["is_anomaly"] & (scored["anomaly_direction"] == "drop")]

    metrics = {
        "model": "IsolationForest",
        "contamination": 0.05,
        "scored_at": datetime.now().isoformat(timespec="seconds"),
        "total_rows": len(scored),
        "anomalies_detected": n_anomalies,
        "anomaly_rate_pct": round((n_anomalies / len(scored)) * 100, 2),
        "spikes": len(spike),
        "drops": len(drop),
        "top_5_spikes": spike.nlargest(5, "daily_revenue")[
            ["order_date", "country_name", "daily_revenue", "anomaly_score"]
        ].to_dict(orient="records"),
        "top_5_drops": drop.nsmallest(5, "daily_revenue")[
            ["order_date", "country_name", "daily_revenue", "anomaly_score"]
        ].to_dict(orient="records"),
        "source": "fact_sales (real)",
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2, default=str)
    log.info("Metrics saved -> %s", METRICS_PATH)
    return metrics


if __name__ == "__main__":
    score_anomalies()
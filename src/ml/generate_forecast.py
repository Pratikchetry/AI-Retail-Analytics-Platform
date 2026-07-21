"""
Phase 0 — AI Retail Intelligence Platform
Real forecast generator.

Uses the trained XGBoost V2 model to forecast future daily revenue.
Recursive multi-step: each day's prediction feeds into the next day's
feature vector. Writes honest forecasts to the revenue_forecast table.
"""

import os
import json
import pickle
from datetime import timedelta

import numpy as np
import pandas as pd
from sqlalchemy import text

from src.utils.db import engine
from src.utils.logger import get_logger

log = get_logger(__name__)

MODEL_PATH = "src/ml/models/forecast_xgb_v2.pkl"
FEATURES_PATH = "src/ml/models/forecast_xgb_v2_features.json"
DEFAULT_HORIZON = 30


def _load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Run: python -m src.ml.train_xgboost_v2"
        )
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


def _load_feature_cols():
    with open(FEATURES_PATH, "r") as f:
        return json.load(f)


def _load_history():
    """Full daily revenue + feature history from the warehouse."""
    log.info("Loading daily revenue history ...")
    with engine.connect() as conn:
        df = pd.read_sql(text("""
            SELECT order_date, daily_revenue, daily_orders,
                   daily_active_customers, avg_transaction_value,
                   largest_single_transaction, large_order_flag,
                   day_of_week, month, week_of_year, is_weekend,
                   is_peak_season, is_public_holiday, holiday_peak_period,
                   revenue_lag_1, revenue_lag_7, revenue_lag_14, revenue_lag_28,
                   orders_lag_1, orders_lag_7, rolling_mean_7, rolling_mean_14,
                   rolling_std_7, rolling_std_14, revenue_growth_7d, orders_growth_7d
            FROM feature_daily_model_input
            ORDER BY order_date
        """), conn)
    log.info("Loaded %d days | last date: %s", len(df), df["order_date"].iloc[-1])
    return df


def _load_holidays():
    """Load UK holiday lookup for feature generation."""
    with engine.connect() as conn:
        rows = pd.read_sql(text(
            "SELECT holiday_date::text, is_public_holiday, is_peak_period "
            "FROM dim_holiday_uk"
        ), conn)
    return {r["holiday_date"]: r for _, r in rows.iterrows()}


def _postgres_dow(date) -> int:
    """Postgres EXTRACT(DOW): 0=Sunday .. 6=Saturday."""
    return (date.weekday() + 1) % 7


def generate_forecast(horizon: int = DEFAULT_HORIZON) -> list[dict]:
    """
    Recursive multi-step forecast for the next `horizon` days.

    Each prediction is appended to the revenue history so that lag and
    rolling features can be recomputed for the subsequent day.
    """
    model = _load_model()
    feature_cols = _load_feature_cols()
    history = _load_history()
    holidays = _load_holidays()

    # ---- Seed arrays from actual history ----
    revenues = history["daily_revenue"].tolist()
    last_date = pd.to_datetime(history["order_date"].iloc[-1])

    # Recent statistics (carried forward for non-forecastable features
    # like daily_orders, avg_transaction_value, growth rates)
    recent = history.tail(28)

    # ---- Recursive forecast loop ----
    log.info("Forecasting %d days from %s ...", horizon, last_date.date() + timedelta(days=1))
    forecasts = []

    for step in range(1, horizon + 1):
        forecast_date = last_date + timedelta(days=step)
        n = len(revenues)

        feat = {}

        # ---- Calendar features (deterministic) ----
        feat["day_of_week"] = _postgres_dow(forecast_date)
        feat["month"] = forecast_date.month
        feat["week_of_year"] = int(forecast_date.strftime("%V"))
        feat["is_weekend"] = feat["day_of_week"] in (0, 6)
        feat["is_peak_season"] = forecast_date.month in (10, 11, 12)

        # ---- Holiday features ----
        h = holidays.get(forecast_date.strftime("%Y-%m-%d"))
        feat["is_public_holiday"] = bool(h["is_public_holiday"]) if h is not None else False
        feat["holiday_peak_period"] = bool(h["is_peak_period"]) if h is not None else False

        # ---- Revenue lag features (actuals then predictions) ----
        feat["revenue_lag_1"] = revenues[n - 1]
        feat["revenue_lag_7"] = revenues[n - 7]
        feat["revenue_lag_14"] = revenues[n - 14]
        feat["revenue_lag_28"] = revenues[n - 28]

        # ---- Rolling features (from actual + predicted history) ----
        feat["rolling_mean_7"] = float(np.mean(revenues[-7:]))
        feat["rolling_mean_14"] = float(np.mean(revenues[-14:]))
        feat["rolling_std_7"] = float(np.std(revenues[-7:]))
        feat["rolling_std_14"] = float(np.std(revenues[-14:]))

        # ---- Order / customer features (carried-forward recent means) ----
        feat["daily_orders"] = float(recent["daily_orders"].mean())
        feat["daily_active_customers"] = float(recent["daily_active_customers"].mean())
        feat["avg_transaction_value"] = float(recent["avg_transaction_value"].mean())
        feat["largest_single_transaction"] = float(recent["largest_single_transaction"].mean())
        feat["large_order_flag"] = 0
        feat["orders_lag_1"] = float(recent["daily_orders"].mean())
        feat["orders_lag_7"] = float(recent["daily_orders"].mean())

        # ---- Growth rates (carry forward — can't compute from unknown present) ----
        feat["revenue_growth_7d"] = float(recent["revenue_growth_7d"].iloc[-1])
        feat["orders_growth_7d"] = float(recent["orders_growth_7d"].iloc[-1])

        # ---- Predict ----
        X = pd.DataFrame([feat])[feature_cols]
        pred = float(model.predict(X)[0])
        pred = max(pred, 0.0)  # revenue cannot be negative

        forecasts.append({
            "forecast_date": (last_date + timedelta(days=step)).strftime("%Y-%m-%d"),
            "forecast_revenue": round(pred, 2),
        })

        # Feed prediction back into history for the next iteration
        revenues.append(pred)

    return forecasts


def save_forecast(forecasts: list[dict], model_name: str = "XGBoost_V2"):
    """Persist forecasts to the revenue_forecast table (replaces mock data)."""
    log.info("Recreating revenue_forecast with correct schema ...")

    # Authoritative schema — immune to leftover mock table from seed_warehouse.py
    CREATE_TABLE_SQL = """
    CREATE TABLE revenue_forecast (
        forecast_date      DATE PRIMARY KEY,
        forecast_revenue   NUMERIC(16,4) NOT NULL,
        model_name         TEXT,
        created_at         TIMESTAMP DEFAULT NOW()
    )
    """
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS revenue_forecast CASCADE"))
        conn.execute(text(CREATE_TABLE_SQL))

    log.info("Writing %d forecast rows to revenue_forecast ...", len(forecasts))
    df = pd.DataFrame(forecasts)
    df["model_name"] = model_name
    df["created_at"] = pd.Timestamp.now()

    df.to_sql("revenue_forecast", engine, if_exists="append", index=False)

    total = sum(f["forecast_revenue"] for f in forecasts)
    avg = total / len(forecasts)
    log.info("Forecast saved | %d days | total £%.2f | avg £%.2f/day",
             len(forecasts), total, avg)
    return df


if __name__ == "__main__":
    forecasts = generate_forecast(horizon=DEFAULT_HORIZON)
    save_forecast(forecasts)
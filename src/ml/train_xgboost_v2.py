"""
Phase 0 — AI Retail Intelligence Platform
Production Forecast Model Training (XGBoost V2) with MLOps (MLflow).

Pulls REAL daily revenue features from the warehouse view
vw_ml_training_data, trains XGBoost, evaluates HONESTLY, and logs
everything to MLflow Tracking + Model Registry.
"""

import os
import json
import pickle
from datetime import datetime

import pandas as pd
import xgboost as xgb
from sqlalchemy import text
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# MLOps imports
import mlflow
import mlflow.xgboost

from src.utils.db import engine
from src.utils.logger import get_logger

log = get_logger(__name__)

# -----------------------------------------------------------
# Paths
# -----------------------------------------------------------
MODEL_DIR = "src/ml/models"
MODEL_PATH = os.path.join(MODEL_DIR, "forecast_xgb_v2.pkl")
FEATURES_PATH = os.path.join(MODEL_DIR, "forecast_xgb_v2_features.json")
METRICS_PATH = "outputs/reports/forecast_summary_xgboost.json"

# MLflow Config
MLFLOW_TRACKING_URI = "http://localhost:5001"
EXPERIMENT_NAME = "Retail_Revenue_Forecasting"

# -----------------------------------------------------------
# Features we train on (must match vw_ml_training_data columns)
# -----------------------------------------------------------
FEATURE_COLS = [
    "daily_orders", "daily_active_customers", "avg_transaction_value",
    "largest_single_transaction", "large_order_flag", "day_of_week",
    "month", "week_of_year", "is_weekend", "is_peak_season",
    "is_public_holiday", "holiday_peak_period",
    "revenue_lag_1", "revenue_lag_7", "revenue_lag_14", "revenue_lag_28",
    "orders_lag_1", "orders_lag_7", "rolling_mean_7", "rolling_mean_14",
    "rolling_std_7", "rolling_std_14", "revenue_growth_7d", "orders_growth_7d",
]

TARGET_COL = "daily_revenue"


def load_training_data() -> pd.DataFrame:
    """Pull the real feature view from the warehouse."""
    log.info("Loading training data from vw_ml_training_data ...")
    with engine.connect() as conn:
        df = pd.read_sql(text("SELECT * FROM vw_ml_training_data ORDER BY order_date"), conn)
    log.info("Loaded %d rows | date range: %s -> %s",
             len(df), df["order_date"].min(), df["order_date"].max())
    return df


def time_based_split(df: pd.DataFrame, test_fraction: float = 0.15):
    """Time-based split (NOT random) — critical for forecasting."""
    df = df.sort_values("order_date").reset_index(drop=True)
    split_idx = int(len(df) * (1 - test_fraction))
    train = df.iloc[:split_idx]
    test = df.iloc[split_idx:]
    log.info("Train: %d rows (%s -> %s)", len(train),
             train["order_date"].min(), train["order_date"].max())
    log.info("Test:  %d rows (%s -> %s)", len(test),
             test["order_date"].min(), test["order_date"].max())
    return train, test


def train_and_evaluate():
    df = load_training_data()
    if df.empty:
        raise RuntimeError("vw_ml_training_data is empty. Run sql/schema/04,05,06 first.")

    df = df.dropna(subset=FEATURE_COLS + [TARGET_COL]).reset_index(drop=True)

    train_df, test_df = time_based_split(df, test_fraction=0.15)

    X_train, y_train = train_df[FEATURE_COLS], train_df[TARGET_COL]
    X_test, y_test = test_df[FEATURE_COLS], test_df[TARGET_COL]

    # XGBoost Parameters (we log these to MLflow)
    params = {
        "n_estimators": 400,
        "max_depth": 6,
        "learning_rate": 0.05,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "random_state": 42,
    }

    # ==========================================
    # MLflow Tracking & Model Registry
    # ==========================================
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    with mlflow.start_run(run_name=f"xgb_v2_train_{datetime.now().strftime('%Y%m%d_%H%M')}") as run:
        log.info("Run ID: %s", run.info.run_id)
        
        # 1. Log parameters
        mlflow.log_params(params)
        mlflow.log_param("features", str(FEATURE_COLS))
        
        log.info("Training XGBoost V2 (Champion forecast model) ...")
        model = xgb.XGBRegressor(**params)
        model.fit(X_train, y_train)

        # 2. Evaluate & Log Metrics
        pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, pred)
        rmse = mean_squared_error(y_test, pred) ** 0.5
        r2 = r2_score(y_test, pred)

        # Naive baseline (predict yesterday's revenue) for comparison
        baseline_pred = test_df["revenue_lag_1"].values
        baseline_mae = mean_absolute_error(y_test, baseline_pred)

        mlflow.log_metric("mae", mae)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("baseline_mae", baseline_mae)
        mlflow.log_metric("improvement_vs_baseline_pct", ((baseline_mae - mae) / baseline_mae) * 100)

        log.info("===== HONEST METRICS (holdout) =====")
        log.info("MAE  : £%.2f", mae)
        log.info("RMSE : £%.2f", rmse)
        log.info("R2   : %.4f", r2)
        log.info("Baseline MAE (lag-1): £%.2f", baseline_mae)

        # 3. Log Model Artifact to MLflow
        mlflow.xgboost.log_model(
            xgb_model=model,
            artifact_path="model",
            registered_model_name="RetailForecastXGBoost"
        )

        # ==========================================
        # Save local artifacts (for the LangGraph Forecast Node)
        # ==========================================
        os.makedirs(MODEL_DIR, exist_ok=True)
        os.makedirs("outputs/reports", exist_ok=True)

        with open(MODEL_PATH, "wb") as f:
            pickle.dump(model, f)

        with open(FEATURES_PATH, "w") as f:
            json.dump(FEATURE_COLS, f, indent=2)

        metrics = {
            "model": "XGBoostRegressor",
            "version": "v2_real",
            "trained_at": datetime.now().isoformat(timespec="seconds"),
            "train_rows": len(train_df),
            "test_rows": len(test_df),
            "holdout_start": str(test_df["order_date"].min()),
            "holdout_end": str(test_df["order_date"].max()),
            "mae": round(mae, 2),
            "rmse": round(rmse, 2),
            "r2": round(r2, 4),
            "baseline_mae": round(baseline_mae, 2),
            "improvement_vs_baseline_pct": round(((baseline_mae - mae) / baseline_mae) * 100, 2),
            "feature_count": len(FEATURE_COLS),
            "top_feature": FEATURE_COLS[int(model.feature_importances_.argmax())],
            "target": TARGET_COL,
            "source_view": "vw_ml_training_data",
            "mlflow_run_id": run.info.run_id
        }
        with open(METRICS_PATH, "w") as f:
            json.dump(metrics, f, indent=2)

        log.info("Model saved -> %s", MODEL_PATH)
        log.info("Metrics saved -> %s", METRICS_PATH)
        log.info("MLflow tracking complete. View at %s", MLFLOW_TRACKING_URI)
        
        return metrics


if __name__ == "__main__":
    train_and_evaluate()
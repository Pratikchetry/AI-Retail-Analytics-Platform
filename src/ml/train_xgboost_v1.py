"""
Phase 2 — AI Retail Intelligence Platform
ML Ops: Training Pipeline Baseline Sales Forecast Model (XGBoost V1).
"""

import os
import pickle
import pandas as pd
import xgboost as xgb

def train_baseline_forecast_pipeline(data_path: str, model_output_path: str):
    """Executes structural baseline data collection, feature formation, and v1 model serialization."""
    print("➔ Loading baseline historical revenue sequences...")
    
    # Mock fallback sequence generator for tracking environment isolation checks
    if not os.path.exists(data_path):
        df = pd.DataFrame({
            "ds": pd.date_range(start="2024-01-01", periods=500, freq="D"),
            "revenue": [10000.0 + (i * 15.0) + (i % 7 * 2000.0) for i in range(500)]
        })
    else:
        df = pd.read_csv(data_path, parse_dates=["ds"])
        
    # Feature Engineering Layer: Basic Timestamps & Simple Historical Lags
    df["lag_7"] = df["revenue"].shift(7)
    df["lag_30"] = df["revenue"].shift(30)
    df = df.dropna()
    
    X = df[["lag_7", "lag_30"]]
    y = df["revenue"]
    
    # Fit Production XGBoost Regressor execution arrays
    print("➔ Fitting Baseline Forecast Engine Regressor V1 (XGBoost)...")
    model_v1 = xgb.XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42)
    model_v1.fit(X, y)
    
    # Secure serialization inside designated models subfolder directory bounds
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    with open(model_output_path, "wb") as f:
        pickle.dump(model_v1, f)
        
    print(f"🎉 Baseline Model V1 saved successfully down to: {model_output_path}")

if __name__ == "__main__":
    train_baseline_forecast_pipeline("assets/features_clean.csv", "src/ml/models/forecast_xgb_v1.pkl")
"""
Phase 2 — AI Retail Intelligence Platform
Integration Test Harness for the Machine Learning Pipeline Submodule.
Validates Anomaly Isolation, XGBoost Training, Binary Storage, and Model Scoring.
"""

import os
import sys
import numpy as np
import pandas as pd

# Automatically append project root to system path to ensure clean internal imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ml.isolation_forest import RetailAnomalyEngine
from src.ml.compare_v1_v2 import ModelEvaluationHarness
from src.ml.train_xgboost_v1 import train_baseline_forecast_pipeline
from src.ml.train_xgboost_v2 import train_advanced_forecast_pipeline

# Isolated asset paths specifically mapped out for the test workspace run
MOCK_CSV_PATH = "assets/test_features_clean.csv"
MODEL_V1_OUT = "src/ml/models/test_forecast_xgb_v1.pkl"
MODEL_V2_OUT = "src/ml/models/test_forecast_xgb_v2.pkl"

def provision_mock_timeseries_data():
    """Generates a localized clean historical CSV footprint to seed the test pipelines."""
    os.makedirs("assets", exist_ok=True)
    np.random.seed(42)
    
    date_range = pd.date_range(start="2025-01-01", periods=100, freq="D")
    base_revenue = [50000.0 + (i * 100.0) + (np.sin(i) * 5000.0) for i in range(100)]
    
    df = pd.DataFrame({"ds": date_range, "revenue": base_revenue})
    
    # Intentionally inject specific extreme outlier boundaries to test the Anomaly Engine
    df.loc[15, "revenue"] = 150000.0  # Big Spike Anomaly
    df.loc[45, "revenue"] = 2000.0    # Massive Drop Anomaly
    
    df.to_csv(MOCK_CSV_PATH, index=False)

def run_ml_pipeline_tests():
    print("=" * 60)
    print("⚡ INITIALIZING PLATFORM ML SUBSYSTEM INTEGRATION TESTS ⚡")
    print("=" * 60)
    
    print("➔ Provisioning Mock Sales Sequences Dataset...")
    provision_mock_timeseries_data()
    
    try:
        # Test Case 1: Validate Isolation Forest Anomaly Engine
        print("\n[Test Case 1] Verifying Isolation Forest Anomaly Logic...")
        df_raw = pd.read_csv(MOCK_CSV_PATH)
        anomaly_engine = RetailAnomalyEngine(contamination=0.05)
        df_anomalies = anomaly_engine.fit_predict_dataframe(df_raw, revenue_col="revenue")
        
        print(f"  • Raw Sequences Count: {len(df_anomalies)}")
        print(f"  • Flagged Anomalies Count: {df_anomalies['is_anomaly'].sum()}")
        
        assert "anomaly_score" in df_anomalies.columns, "Failed: 'anomaly_score' metric missing."
        assert df_anomalies["is_anomaly"].sum() > 0, "Failed: Engine missed the artificial outliers."
        print("  Status: PASSED ✓")
        
        # Test Case 2: Validate XGBoost Baseline V1 Pipeline
        print("\n[Test Case 2] Verifying XGBoost V1 Model Training and Serialization...")
        train_baseline_forecast_pipeline(data_path=MOCK_CSV_PATH, model_output_path=MODEL_V1_OUT)
        
        assert os.path.exists(MODEL_V1_OUT), "Failed: V1 binary wasn't written to disk."
        print("  Status: PASSED ✓")
        
        # Test Case 3: Validate XGBoost Champion V2 Pipeline
        print("\n[Test Case 3] Verifying XGBoost V2 Tuning and Serialization...")
        train_advanced_forecast_pipeline(data_path=MOCK_CSV_PATH, model_output_path=MODEL_V2_OUT)
        
        assert os.path.exists(MODEL_V2_OUT), "Failed: V2 champion binary wasn't written to disk."
        print("  Status: PASSED ✓")
        
        # Test Case 4: Validate Performance Matrix Comparison Evaluation
        print("\n[Test Case 4] Verifying Statistical Evaluation Harness metrics...")
        harness = ModelEvaluationHarness()
        
        mock_ground_truth = np.array([60000.0, 62000.0, 65000.0])
        mock_pred_v1 = np.array([55000.0, 58000.0, 72000.0])
        mock_pred_v2 = np.array([59500.0, 61200.0, 64200.0])
        
        metrics = harness.evaluate_model_variants(mock_ground_truth, mock_pred_v1, mock_pred_v2)
        print(f"  • Model V1 Baseline MAE: ${metrics['v1_baseline']['mae']}")
        print(f"  • Model V2 Champion MAE: ${metrics['v2_champion']['mae']}")
        print(f"  • Error Reduction Efficiency Gain: {metrics['efficiency_gain_pct']}%")
        
        assert metrics["v2_champion"]["mae"] < metrics["v1_baseline"]["mae"], "Failed: V2 accuracy tracking error check."
        print("  Status: PASSED ✓")
        
        print("\n" + "=" * 60)
        print("🎉 ALL CORE ML OPS COMPONENT TESTS PASSED SUCCESSFULLY! 🎉")
        print("=" * 60)
        
    finally:
        # Systematic environment cleanup routine
        for path in [MOCK_CSV_PATH, MODEL_V1_OUT, MODEL_V2_OUT]:
            if os.path.exists(path):
                os.remove(path)

if __name__ == "__main__":
    run_ml_pipeline_tests()
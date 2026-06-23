"""
Phase 2 — AI Retail Intelligence Platform
ML Ops: Model Comparison Evaluation Harness (V1 Baseline vs V2 Champion).
Calculates corporate error matrices to evaluate pipeline deployment eligibility.
"""

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

class ModelEvaluationHarness:
    @staticmethod
    def calculate_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Computes Mean Absolute Percentage Error. Handles zero denominators safely using clipping."""
        # Use np.clip to prevent division-by-zero errors if true values contain zeroes
        safe_y_true = np.clip(np.abs(y_true), 1e-5, None)
        return float(np.mean(np.abs((y_true - y_pred) / safe_y_true)) * 100.0)

    def evaluate_model_variants(self, y_true: np.ndarray, v1_predictions: np.ndarray, v2_predictions: np.ndarray) -> dict:
        """Performs statistical analytics across models to generate clear comparison profiles."""
        
        metrics = {
            "v1_baseline": {
                "mae": round(float(mean_absolute_error(y_true, v1_predictions)), 2),
                "rmse": round(float(np.sqrt(mean_squared_error(y_true, v1_predictions))), 2),
                "mape": round(self.calculate_mape(y_true, v1_predictions), 2)
            },
            "v2_champion": {
                "mae": round(float(mean_absolute_error(y_true, v2_predictions)), 2),
                "rmse": round(float(np.sqrt(mean_squared_error(y_true, v2_predictions))), 2),
                "mape": round(self.calculate_mape(y_true, v2_predictions), 2)
            }
        }
        
        # Determine performance delta improvement shift scale
        v1_mae = metrics["v1_baseline"]["mae"]
        v2_mae = metrics["v2_champion"]["mae"]
        
        if v1_mae > 0:
            metrics["efficiency_gain_pct"] = round(((v1_mae - v2_mae) / v1_mae) * 100.0, 2)
        else:
            metrics["efficiency_gain_pct"] = 0.0
        
        return metrics

if __name__ == "__main__":
    # Sanity baseline print verification testing routine
    harness = ModelEvaluationHarness()
    mock_true = np.array([10000.0, 15000.0, 20000.0])
    mock_v1 = np.array([11000.0, 13500.0, 22000.0])
    mock_v2 = np.array([10200.0, 14700.0, 20100.0])
    
    report = harness.evaluate_model_variants(mock_true, mock_v1, mock_v2)
    print("📊 Evaluation Report Generated:")
    print(f"  • V1 Baseline MAE: {report['v1_baseline']['mae']}")
    print(f"  • V2 Champion MAE: {report['v2_champion']['mae']}")
    print(f"  • System Error Reduction Delta: {report['efficiency_gain_pct']}%")
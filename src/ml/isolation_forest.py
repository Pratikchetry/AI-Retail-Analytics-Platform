"""
Phase 2 — AI Retail Intelligence Platform
ML Ops: Isolation Forest Unsupervised Anomaly Detection Engine.
Identifies statistical drift and extreme revenue drops/spikes.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

class RetailAnomalyEngine:
    def __init__(self, contamination: float = 0.05, random_state: int = 42):
        """
        Initializes the unsupervised outlier detection model.
        contamination: The expected proportion of outliers in the data footprint.
        """
        self.model = IsolationForest(contamination=contamination, random_state=random_state)
        
    def fit_predict_dataframe(self, df: pd.DataFrame, revenue_col: str = "daily_revenue") -> pd.DataFrame:
        """
        Accepts historical revenue time-series data, fits an IsolationForest,
        and computes operational baseline scores and anomaly tracking flags.
        """
        if df.empty or revenue_col not in df.columns:
            raise ValueError(f"Target vector column '{revenue_col}' missing or dataset empty.")
            
        processed_df = df.copy()
        
        # Reshape targeted feature space array for isolation fitting matrixes
        X = processed_df[[revenue_col]].values
        
        # Fit model pipeline routines
        # IsolationForest returns -1 for outliers and 1 for normal data points
        predictions = self.model.fit_predict(X)
        scores = self.model.decision_function(X) # Higher score = more normal; lower = more anomalous
        
        # Synthesize canonical outputs matching our core data warehouse schemas
        processed_df["anomaly_score"] = np.round(1.0 - scores, 4) # Invert scale: higher = more volatile
        processed_df["is_anomaly"] = np.where(predictions == -1, True, False)
        
        # Calculate moving baseline expectations dynamically via rolling clean window values
        rolling_baseline = processed_df[revenue_col].rolling(window=7, min_periods=1, center=True).median()
        processed_df["expected_baseline"] = np.round(rolling_baseline, 2)
        
        # Categorize drift direction
        processed_df["anomaly_direction"] = np.where(
            ~processed_df["is_anomaly"], "stable",
            np.where(processed_df[revenue_col] > processed_df["expected_baseline"], "spike", "drop")
        )
        
        return processed_df
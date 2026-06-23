"""
Phase 5 — AI Retail Intelligence Platform
Database Migration and Seed Utility.
Creates tables and populates retail_db with mock revenue and anomaly metrics.
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from src.executor.query_executor import QueryExecutionEngine

def seed_retail_warehouse():
    print("\n============================================================")
    print("🗄️ SEEDING LOCAL POSTGRESQL RETAIL WAREHOUSE")
    print("============================================================")
    
    # 1. Initialize the existing query engine to reuse your validated connection url
    try:
        engine = QueryExecutionEngine().engine
    except Exception as e:
        print(f"❌ Failed to connect to database engine: {e}")
        return

    # 2. Build mock dataset for ml_anomaly_scores
    print("📦 Generating mock analytical data...")
    base_date = datetime.now() - timedelta(days=30)
    
    data = []
    countries = ["India", "United States", "United Kingdom", "Germany", "Japan"]
    
    for i in range(100):
        record_date = (base_date + timedelta(days=i // 4)).strftime("%Y-%m-%d")
        country = countries[i % len(countries)]
        daily_revenue = 5000.00 + (i * 120.50)
        
        # Inject an obvious high-risk anomaly at index 42
        if i == 42:
            anomaly_score = 0.98
            daily_revenue *= 3.5  # Revenue spike
        else:
            anomaly_score = round(0.1 + (i % 10) * 0.05, 2)
            
        data.append({
            "date": record_date,  # This perfectly fixes the missing 'date' column!
            "country_name": country,
            "daily_revenue": round(daily_revenue, 2),
            "anomaly_score": anomaly_score
        })
        
    df = pd.DataFrame(data)

    # 3. Write data frames to PostgreSQL instance
    try:
        with engine.begin() as connection:
            # Ensure an old broken table layout gets cleared out
            connection.execute(text("DROP TABLE IF EXISTS ml_anomaly_scores;"))
            print("🧹 Cleared old 'ml_anomaly_scores' table definitions.")
            
        # Write the dataframe as a fresh table schema
        df.to_sql("ml_anomaly_scores", con=engine, if_exists="replace", index=False)
        print(f"✅ Successfully created table and seeded {len(df)} sample operational records!")
        
    except Exception as e:
        print(f"❌ Migration block encountered database failure: {e}")

if __name__ == "__main__":
    seed_retail_warehouse()
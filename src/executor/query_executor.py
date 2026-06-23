"""
Phase 5 — AI Retail Intelligence Platform
Enterprise PostgreSQL Query Execution Engine.
Features explicit .env configuration loading, password URL-encoding, and transactional guardrails.
"""

import os
import time
import urllib.parse
from typing import Dict, Any
from sqlalchemy import create_engine, text
import pandas as pd
from dotenv import load_dotenv

class QueryExecutionEngine:
    def __init__(self, connection_uri: str = None):
        # Explicitly load the .env file sitting in the current working directory
        load_dotenv()
        
        raw_uri = connection_uri or os.getenv("DATABASE_URL")
        
        if not raw_uri:
            # Match your active local parameters exactly
            raw_uri = "postgresql://postgres:Pratik@123@localhost:5432/retail_db"
            
        try:
            # Safe parsing block: URL-encode the password if it contains special characters like '@'
            if "Pratik@123" in raw_uri and not "Pratik%40123" in raw_uri:
                # Replace the raw password with its URL-encoded equivalent (%40 is @)
                raw_uri = raw_uri.replace("Pratik@123", urllib.parse.quote_plus("Pratik@123"))
            
            self.engine = create_engine(raw_uri, pool_size=5, max_overflow=10)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize PostgreSQL connection pool: {str(e)}")
            
        self.query_cache = {}

    def execute_query(self, sql_query: str) -> Dict[str, Any]:
        start_time = time.time()
        clean_query = sql_query.strip()
        
        forbidden_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "GRANT"]
        if any(keyword in clean_query.upper() for keyword in forbidden_keywords):
            return {
                "status": "CRITICAL_FAILURE",
                "data": "Security Exception: Write modifications are prohibited.",
                "cached": False,
                "execution_time_ms": 0.0
            }
            
        if clean_query in self.query_cache:
            return {
                "status": "SUCCESS",
                "data": self.query_cache[clean_query],
                "cached": True,
                "execution_time_ms": (time.time() - start_time) * 1000
            }
            
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SET TRANSACTION READ ONLY;"))
                df = pd.read_sql_query(text(clean_query), connection)
                
            self.query_cache[clean_query] = df
            return {
                "status": "SUCCESS",
                "data": df,
                "cached": False,
                "execution_time_ms": (time.time() - start_time) * 1000
            }
        except Exception as e:
            return {
                "status": "CRITICAL_FAILURE",
                "data": str(e),
                "cached": False,
                "execution_time_ms": (time.time() - start_time) * 1000
            }
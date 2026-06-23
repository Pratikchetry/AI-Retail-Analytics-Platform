"""
Phase 2 — AI Retail Intelligence Platform
Integration Test Harness for the Data Routing & Execution Engine.
Spins up a localized File-Backed Mock Warehouse to guarantee connection state sharing.
"""

import os
import sys
import sqlite3
import pandas as pd

# Automatically append project root to system path to ensure clean internal imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.executor.query_router import QueryRouter
from src.executor.query_executor import QueryExecutionEngine

TEST_DB_PATH = ".test_warehouse.db"

def setup_mock_data_warehouse(db_path: str):
    """Spins up a local file-based SQLite database populated with core retail views."""
    # Wipe any stale test database remnant if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Create Mock ML Anomaly Scores view/table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ml_anomaly_scores (
            date TEXT,
            country_name TEXT,
            daily_revenue REAL,
            expected_baseline REAL,
            anomaly_score REAL,
            is_anomaly INTEGER,
            anomaly_direction TEXT
        )
    """)
    cursor.executemany("""
        INSERT INTO ml_anomaly_scores VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        ("2026-06-01", "United Kingdom", 120500.0, 85000.0, 0.89, 1, "spike"),
        ("2026-06-02", "Germany", 14000.0, 45000.0, 0.94, 1, "drop"),
        ("2026-06-03", "France", 52000.0, 50000.0, 0.12, 0, "stable")
    ])

    # 2. Create Mock Customer Segment Revenue view/table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_segment_revenue (
            customer_segment TEXT,
            customer_count INTEGER,
            total_revenue REAL,
            avg_order_revenue REAL
        )
    """)
    cursor.executemany("""
        INSERT INTO customer_segment_revenue VALUES (?, ?, ?, ?)
    """, [
        ("Champions", 1250, 450000.0, 360.0),
        ("At Risk", 840, 120000.0, 142.8),
        ("Hibernating", 2300, 45000.0, 19.5)
    ])

    conn.commit()
    conn.close()

def run_integration_test_suite():
    print("=" * 60)
    print("⚡ INITIALIZING PLATFORM ENGINE INTEGRATION TESTS ⚡")
    print("=" * 60)

    print("➔ Provisioning File-Backed Mock Analytical Warehouse...")
    setup_mock_data_warehouse(TEST_DB_PATH)
    
    try:
        # Initialize Core Components pointing to our isolated file
        router = QueryRouter()
        executor = QueryExecutionEngine(db_path=TEST_DB_PATH, cache_ttl_seconds=10)
        
        # Test Case 1: Validate Fast-Track Static Routing
        print("\n[Test Case 1] Verifying Semantic Keyword Intent Routing...")
        user_voice_input = "Hey copilot, check if we have any active anomalies or market outliers right now?"
        route_type, payload, metadata = router.route_intent(user_voice_input)
        
        print(f"  • Input Utterance: '{user_voice_input}'")
        print(f"  • Determined Route: {route_type}")
        print(f"  • Matched Key: {metadata.get('matched_key')}")
        assert route_type == "STATIC", "Failed: Anomaly keywords should map to STATIC route shortcut."
        assert metadata["matched_key"] == "all_active_anomalies", "Failed: Incorrect metric key assignment."
        print("  Status: PASSED ✓")

        # Test Case 2: Validate Raw Query Execution
        print("\n[Test Case 2] Verifying SQL Execution over Data Warehouse Views...")
        result = executor.execute_query(payload)
        print(f"  • Execution Status: {result['status']}")
        if result['status'] == "CRITICAL_FAILURE":
            print(f"    Error Log: {result['data']}")
        print(f"  • Rows Retrieved: {len(result['data']) if isinstance(result['data'], pd.DataFrame) else 0}")
        print(f"  • Caching Status (Initial Run): {result['cached']}")
        
        assert result["status"] == "SUCCESS", f"Failed to execute query: {result['data']}"
        assert isinstance(result["data"], pd.DataFrame), "Returned dataset must be a Pandas DataFrame."
        assert len(result["data"]) == 2, "Should have filtered exactly 2 active anomalies."
        print("  Status: PASSED ✓")

        # Test Case 3: Validate High-Speed In-Memory Caching (TTL)
        print("\n[Test Case 3] Verifying Time-To-Live (TTL) Caching Performance...")
        cached_result = executor.execute_query(payload)
        print(f"  • Caching Status (Second Run): {cached_result['cached']}")
        print(f"  • Initial Latency: {result['execution_time_ms']} ms")
        print(f"  • Cached Latency: {cached_result['execution_time_ms']} ms")
        assert cached_result["cached"] is True, "The execution engine failed to intercept with cache."
        print("  Status: PASSED ✓")

        # Test Case 4: Validate Dynamic Agent Delegation Fallback
        print("\n[Test Case 4] Verifying Dynamic Agent Graph Fallback Routing...")
        unseen_complex_prompt = "Compare the lifetime value of users who bought shoes vs those who bought hats in Q1."
        route_type, payload, metadata = router.route_intent(unseen_complex_prompt)
        print(f"  • Input Utterance: '{unseen_complex_prompt}'")
        print(f"  • Determined Route: {route_type}")
        print(f"  • Internal Strategy: {metadata.get('strategy')}")
        assert route_type == "DYNAMIC_AGENT", "Failed: Complex unique prompts should cascade down to Agent Graph."
        print("  Status: PASSED ✓")

        print("\n" + "=" * 60)
        print("🎉 ALL PLATFORM INFRASTRUCTURE TESTS PASSED SUCCESSFULLY! 🎉")
        print("=" * 60)

    finally:
        # Safe breakdown cleanup: drop the temporary test file out of the root folder
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

if __name__ == "__main__":
    run_integration_test_suite()
# tests/test_rag.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.executor.query_executor import QueryExecutionEngine
from src.rag.index_schemas import build_and_seed_vector_warehouse
from src.rag.retriever import MetadataGroundingRetriever
from src.rag.embedder import LocalTextEmbedder

def run_rag_production_test():
    print("\n============================================================")
    print("⚡ TESTING ENTERPRISE POSTGRESQL RAG GROUNDING SUITE ⚡")
    print("============================================================")
    
    # 1. Initialize Executor Pool and the Authenticated Embedder
    executor = QueryExecutionEngine()
    embedder = LocalTextEmbedder()  # Spin up the authenticated engine first
    
    # 2. Build and Seed Warehouse using our shared engine
    print("[Test Case 1] Seeding vector space with PostgreSQL schemas...")
    v_db = build_and_seed_vector_warehouse(executor, embedder)  # Pass the authenticated embedder here!
    print("  Status: PASSED ✓")
    
    # 3. Test Retrieval
    print("[Test Case 2] Evaluating semantic retrieval lookups...")
    retriever = MetadataGroundingRetriever(v_db, embedder)
    
    context = retriever.retrieve_grounding_context("Show me daily anomalies", top_k=1)
    assert context is not None
    print("  Status: PASSED ✓")
    print("\n🎉 ALL CORE RAG GROUNDING TESTS PASSED CLEANLY!")

if __name__ == "__main__":
    run_rag_production_test()
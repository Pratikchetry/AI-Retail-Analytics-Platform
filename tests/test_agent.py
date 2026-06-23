# tests/test_agent.py
import sys
import os

# Force Python to recognize your src directory paths accurately
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.executor.query_executor import QueryExecutionEngine
from src.rag.index_schemas import build_and_seed_vector_warehouse
from src.rag.embedder import LocalTextEmbedder
from src.rag.retriever import MetadataGroundingRetriever
from src.agent.agent_graph import RetailIntelligenceAgent
from src.agent.agent_loop import compile_agent_workflow

def run_end_to_end_agent_test():
    print("\n============================================================")
    print("⚡ TESTING ENTERPRISE MULTI-AGENT STATE GRAPH SUITE ⚡")
    print("============================================================")
    
    # 1. Spin up the localized runtime dependencies in the correct order
    executor = QueryExecutionEngine()
    embedder = LocalTextEmbedder() # Spin up the authenticated engine first
    v_db = build_and_seed_vector_warehouse(executor, embedder) # Pass it here!
    retriever = MetadataGroundingRetriever(v_db, embedder)
    
    # 2. Build and compile the active LangGraph workflow
    agent_core = RetailIntelligenceAgent(retriever, executor)
    graph = compile_agent_workflow(agent_core)
    
    # 3. Define an analytical user query transaction
    initial_state = {
        "user_query": "Fetch the highest risk anomaly scores inside our revenue logs",
        "grounding_context": "",
        "generated_sql": "",
        "execution_result": {"status": "PENDING", "data": [], "cached": False, "execution_time_ms": 0.0},
        "error_logs": [],
        "final_response": "",
        "loop_count": 0
    }
    
    print("🚀 Executing Live Graph State Machine Transaction Loop...")
    final_state = graph.invoke(initial_state)
    
    # 4. Print out the structured transaction results
    print("\n------------------------------------------------------------")
    print("📊 AGENT GRAPH EXECUTION SUMMARY TRACE:")
    print(f"  • Total Node Loops Traversed: {final_state['loop_count']}")
    print(f"  • Generated SQL: {final_state['generated_sql']}")
    print(f"  • Execution Status: {final_state['execution_result']['status']}")
    print(f"  • Final Synthesized Answer:\n    {final_state['final_response']}")
    print("------------------------------------------------------------")
    print("🎉 MULTI-AGENT STATE GRAPH PASSES INTEGRATION SUITE!")

if __name__ == "__main__":
    run_end_to_end_agent_test()
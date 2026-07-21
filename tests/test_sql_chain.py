"""
Smoke test: router -> rag -> sql_gen -> sql_validate -> sql_exec.
Tests one SQL_LOOKUP question end-to-end through the chain.
"""

from src.langgraph.nodes.router_node import router_node
from src.langgraph.nodes.rag_retriever_node import rag_retriever_node
from src.langgraph.nodes.sql_generator_node import sql_generator_node
from src.langgraph.nodes.sql_validator_node import sql_validator_node
from src.langgraph.nodes.sql_executor_node import sql_executor_node


def main():
    question = "Which country had the highest average order value?"

    print("=== SQL Chain Smoke Test ===")
    print(f"Q: {question}\n")

    # Step 1: Route
    state = {"question": question}
    state.update(router_node(state))
    print(f"Route: {state['route']}")

    if state["route"] != "SQL_LOOKUP":
        print("Not a SQL question — skipping chain test")
        return

    # Step 2: RAG
    state.update(rag_retriever_node(state))
    print(f"Context: {len(state['context'])} chars retrieved")

    # Step 3: SQL Generate
    state.update(sql_generator_node(state))
    print(f"SQL: {state['sql'][:120]}")

    # Step 4: Validate
    state.update(sql_validator_node(state))
    print(f"Valid: {state['is_valid']}")

    if not state["is_valid"]:
        print(f"Errors: {state['validation_errors']}")
        return

    # Step 5: Execute
    state.update(sql_executor_node(state))
    print(f"Status: {state['execution_status']}")
    print(f"Result: {str(state['rows'])[:200]}")

    print("\n=== Chain test complete ===")


if __name__ == "__main__":
    main()
"""
Smoke test: full reasoning chain for a SQL question.
Reasoning → Recommendation → Critic.
"""

from src.langgraph.nodes.rag_retriever_node import rag_retriever_node
from src.langgraph.nodes.sql_generator_node import sql_generator_node
from src.langgraph.nodes.sql_validator_node import sql_validator_node
from src.langgraph.nodes.sql_executor_node import sql_executor_node
from src.langgraph.nodes.reasoning_node import reasoning_node
from src.langgraph.nodes.recommendation_node import recommendation_node
from src.langgraph.nodes.critic_node import critic_node


def main():
    question = "Which country had the highest average order value?"

    print("=== Reasoning Chain Smoke Test ===")
    print(f"Q: {question}\n")

    state = {"question": question, "route": "SQL_LOOKUP"}

    # RAG + SQL chain
    state.update(rag_retriever_node(state))
    state.update(sql_generator_node(state))
    state.update(sql_validator_node(state))
    state.update(sql_executor_node(state))
    print(f"SQL valid: {state['is_valid']}")
    print(f"Status: {state['execution_status']}")

    # Reasoning
    state.update(reasoning_node(state))
    print(f"\n--- ANSWER ---\n{state['answer']}")

    # Recommendation
    state.update(recommendation_node(state))
    print(f"\n--- RECOMMENDATION ---\n{state['recommendation']}")

    # Critic
    state.update(critic_node(state))
    print(f"\n--- CRITIC ---")
    print(f"Score: {state['critic_score']:.2f} | Passes: {state['critic_passes']}")
    print(f"Feedback: {state['critic_feedback']}")

    print("\n=== Chain test complete ===")


if __name__ == "__main__":
    main()
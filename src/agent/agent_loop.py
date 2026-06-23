"""
Phase 5 — AI Retail Intelligence Platform
LangGraph Adaptive State Machine Core Orchestrator.
"""

from langgraph.graph import StateGraph, END

from src.agent.agent_graph import (
    AgentState,
    RetailIntelligenceAgent
)


def compile_agent_workflow(
    agent_core: RetailIntelligenceAgent
):

    workflow = StateGraph(
        AgentState
    )

    workflow.add_node(
        "planner_retriever",
        agent_core.node_planner_retriever
    )

    workflow.add_node(
        "sql_specialist",
        agent_core.node_sql_specialist
    )

    workflow.add_node(
        "sql_validator",
        agent_core.node_sql_validator
    )

    workflow.add_node(
        "query_executor",
        agent_core.node_query_executor
    )

    workflow.add_node(
        "response_synthesizer",
        agent_core.node_response_synthesizer
    )

    workflow.set_entry_point(
        "planner_retriever"
    )

    workflow.add_edge(
        "planner_retriever",
        "sql_specialist"
    )

    workflow.add_edge(
        "sql_specialist",
        "sql_validator"
    )

    workflow.add_edge(
        "sql_validator",
        "query_executor"
    )

    workflow.add_conditional_edges(
        "query_executor",
        agent_core.routing_check,
        {
            "fix_query": "sql_specialist",
            "synthesize": "response_synthesizer"
        }
    )

    workflow.add_edge(
        "response_synthesizer",
        END
    )

    return workflow.compile()
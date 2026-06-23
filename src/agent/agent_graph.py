"""
Phase 5 — AI Retail Intelligence Platform
Enterprise Agent Core Nodes.
"""

from typing import Dict, Any, TypedDict, List

from src.llm.groq_client import GroqClient
from src.llm.prompt_templates import SQL_GENERATION_TEMPLATE
from src.agent.sql_validator import SQLValidator


class AgentState(TypedDict):
    user_query: str
    grounding_context: str
    generated_sql: str
    validation_result: Dict[str, Any]
    execution_result: Dict[str, Any]
    error_logs: List[str]
    final_response: str
    loop_count: int


class RetailIntelligenceAgent:

    def __init__(self, retriever, executor):

        self.retriever = retriever
        self.executor = executor

        self.llm = GroqClient()
        self.validator = SQLValidator()

        self.max_loops = 2

    def node_planner_retriever(
        self,
        state: AgentState
    ) -> Dict[str, Any]:

        context = self.retriever.retrieve_grounding_context(
            state["user_query"],
            top_k=5
        )

        return {
            "grounding_context": context,
            "loop_count": 0,
            "error_logs": []
        }

    def node_sql_specialist(
        self,
        state: AgentState
    ) -> Dict[str, Any]:

        current_loop = state.get(
            "loop_count",
            0
        ) + 1

        prompt = SQL_GENERATION_TEMPLATE.format(
            user_question=state["user_query"],
            context=state["grounding_context"]
        )

        generated_sql = self.llm.generate_response(
            prompt
        )

        generated_sql = (
            generated_sql
            .replace("```sql", "")
            .replace("```", "")
            .strip()
        )

        return {
            "generated_sql": generated_sql,
            "loop_count": current_loop
        }

    def node_sql_validator(
        self,
        state: AgentState
    ) -> Dict[str, Any]:

        validation = self.validator.validate(
            state["user_query"],
            state["generated_sql"]
        )

        errors = list(
            state.get(
                "error_logs",
                []
            )
        )

        if not validation["valid"]:

            errors.extend(
                validation["errors"]
            )

        return {
            "validation_result": validation,
            "error_logs": errors
        }

    def node_query_executor(
        self,
        state: AgentState
    ) -> Dict[str, Any]:

        validation = state.get(
            "validation_result",
            {}
        )

        if not validation.get(
            "valid",
            True
        ):

            return {
                "execution_result": {
                    "status": "CRITICAL_FAILURE",
                    "data": (
                        "Business Rule Validation Failed: "
                        + "; ".join(
                            validation["errors"]
                        )
                    ),
                    "cached": False,
                    "execution_time_ms": 0.0
                }
            }

        output = self.executor.execute_query(
            state["generated_sql"]
        )

        errors = list(
            state.get(
                "error_logs",
                []
            )
        )

        if output["status"] == "CRITICAL_FAILURE":

            errors.append(
                str(
                    output["data"]
                )
            )

        return {
            "execution_result": output,
            "error_logs": errors
        }

    def node_response_synthesizer(
        self,
        state: AgentState
    ) -> Dict[str, Any]:

        result = state["execution_result"]

        if result["status"] == "SUCCESS":

            summary = (
                f"Analysis compiled successfully.\n\n"
                f"Rows Retrieved: {len(result['data'])}\n"
                f"Execution Time: "
                f"{round(result['execution_time_ms'], 2)} ms\n"
                f"Cached: {result['cached']}"
            )

        else:

            summary = (
                f"Execution failed.\n\n"
                f"Reason:\n"
                f"{state['error_logs'][-1]}"
            )

        return {
            "final_response": summary
        }

    def routing_check(
        self,
        state: AgentState
    ) -> str:

        validation = state.get(
            "validation_result",
            {}
        )

        if (
            validation
            and not validation.get(
                "valid",
                True
            )
            and state.get(
                "loop_count",
                0
            ) < self.max_loops
        ):

            print(
                f"⚠️ Validation failed. "
                f"Loop {state['loop_count']}"
            )

            return "fix_query"

        if (
            state["execution_result"]["status"]
            == "CRITICAL_FAILURE"
            and state.get(
                "loop_count",
                0
            ) < self.max_loops
        ):

            print(
                f"⚠️ Execution failed. "
                f"Loop {state['loop_count']}"
            )

            return "fix_query"

        return "synthesize"
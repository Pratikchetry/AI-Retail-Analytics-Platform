from src.agent.intent_agent import IntentAgent
from src.agent.context_agent import ContextAgent
from src.agent.sql_agent import SQLAgent
from src.agent.validation_agent import ValidationAgent
from src.agent.business_reasoning_agent import BusinessReasoningAgent

from src.executor.query_executor import (
    QueryExecutionEngine
)

from src.agent.execution_validator import (
    ExecutionValidator
)

def main():

    intent_agent = IntentAgent()
    context_agent = ContextAgent()
    sql_agent = SQLAgent()
    validation_agent = ValidationAgent()
    executor = QueryExecutionEngine()
    execution_validator = (
        ExecutionValidator()
    )
    reasoning_agent = (
        BusinessReasoningAgent()
    )
    questions = [
        "Which customer segment generates most revenue?",
        "What is the only true Superstar product?",
        "Why did YoY show negative growth?",
        "What month is operationally critical?",
        "What was TikTok advertising revenue?",
        "What is customer lifetime value?"
    ]
    for q in questions:
        print("\n")
        print("=" * 120)
        print("QUESTION")
        print("=" * 120)
        print(q)
        # =================================================
        # Intent Classification
        # =================================================
        intent = intent_agent.classify(q)
        print("\nINTENT")
        print("-" * 80)
        print(intent)
        # =================================================
        # Context Retrieval
        # =================================================
        context_result = context_agent.get_context(
            q,
            intent,
            top_k=8
        )
        print("\nCONTEXT PREVIEW")
        print("-" * 80)
        print(
            context_result.context[:1000]
        )
        # =================================================
        # SQL Generation
        # =================================================
        sql_result = (
            sql_agent.generate_sql(q)
        )
        print("\nSQL")
        print("-" * 80)
        print(sql_result.sql)
        print("\nSQL EXPLANATION")
        print("-" * 80)
        print(sql_result.explanation)
        print("\nSQL CONFIDENCE")
        print("-" * 80)
        print(sql_result.confidence)
        # =================================================
        # Validation Layer
        # =================================================
        validation_result = (
            validation_agent.validate(
                sql=sql_result.sql,
                question=q,
                context=context_result.context
            )
        )
        print("\nVALIDATION")
        print("-" * 80)
        print(validation_result)
        if not validation_result.is_valid:
            print("\nVALIDATION FAILED")
            print(
                validation_result.errors
            )
            continue
        
        # =================================================
        # SQL Execution
        # =================================================
        sql_to_execute = sql_result.sql.strip()
        if sql_to_execute in ("NO_SQL_REQUIRED", "INFORMATION_NOT_AVAILABLE"):
            print("\nEXECUTION")
            print("-" * 80)
            print("SKIPPED")
            data = sql_to_execute
        else:
            execution_result = (
                executor.execute_query(
                    sql_result.sql
                )
            )
            print("\nEXECUTION")
            print("-" * 80)
            print(
                execution_result["status"]
            )
            if (
                execution_result["status"]
                != "SUCCESS"
            ):
                print(
                    execution_result["data"]
                )
                continue
            data = (
                execution_result["data"]
            )
            if hasattr(data, "head"):
                print("\nRESULT SAMPLE")
                print("-" * 80)
                print(data.head(10))
            
            # =================================================
            # Execution Validation
            # =================================================
            execution_validation = (
                execution_validator.validate(
                    question=q,
                    sql=sql_result.sql,
                    execution_result=data
                )
            )
            print("\nEXECUTION VALIDATION")
            print("-" * 80)
            print(execution_validation)
            if not execution_validation.valid:
                print("\nBLOCKED")
                print(
                    execution_validation.errors
                )
                continue

        # =================================================
        # Business Reasoning
        # =================================================
        if isinstance(data, str):
            sql_result_str = data
        else:
            try:
                sql_result_str = data.to_string(index=False)
            except AttributeError:
                sql_result_str = str(data)
                
        print("\nPASSING SQL TO REASONING:")
        print("-" * 80)
        print(sql_result_str)
            
        reasoning_result = (
            reasoning_agent.reason(
                q,
                context_result.context,
                sql_result=sql_result_str
            )
        )
        print("\nANSWER")
        print("-" * 80)
        print(reasoning_result.answer)
        print("\nREASONING")
        print("-" * 80)
        print(reasoning_result.reasoning)
        print("\nEVIDENCE")
        print("-" * 80)
        print(reasoning_result.evidence)
        print("\nCONFIDENCE")
        print("-" * 80)
        print(reasoning_result.confidence)
        print("\n")
        print("=" * 120)
        print("FULL PIPELINE TEST COMPLETED")
        print("=" * 120)

if __name__ == "__main__":
    main()
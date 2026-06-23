from src.agent.execution_validator import (
    ExecutionValidator
)

validator = ExecutionValidator()

result = validator.validate(
    question="What is customer lifetime value?",
    sql="INFORMATION_NOT_AVAILABLE",
    execution_result=[]
)

print(result)
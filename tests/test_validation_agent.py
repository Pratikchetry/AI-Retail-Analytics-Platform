from src.agent.validation_agent import (
    ValidationAgent
)

validator = ValidationAgent()

question = (
    "What is the only true Superstar product?"
)

context = """
Customer revenue report.

No product ranking exists.

No business findings available.

"""

sql = """
SELECT stock_code
FROM dim_product
"""

result = validator.validate(
    sql=sql,
    question=question,
    context=context
)

print("\nVALIDATION RESULT")
print("=" * 60)

print(result)

assert result.is_valid is False

assert any(
    "Superstar"
    in error
    for error in result.errors
)

print("\nPASS")
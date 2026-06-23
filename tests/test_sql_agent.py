from src.agent.sql_agent import SQLAgent

agent = SQLAgent()

question = (
    "Which customer segment generates most revenue?"
)

result = agent.generate_sql(
    question
)

print("\nSQL")
print("=" * 80)
print(result.sql)

print("\nEXPLANATION")
print("=" * 80)
print(result.explanation)

print("\nCONFIDENCE")
print("=" * 80)
print(result.confidence)
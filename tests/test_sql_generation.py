from src.llm.groq_client import GroqClient
from src.llm.prompt_templates import SQL_GENERATION_TEMPLATE


client = GroqClient()

prompt = SQL_GENERATION_TEMPLATE.format(
    user_question="Show revenue trend",
    context="""
Table: revenue_growth_analysis
Columns:
month_date
total_revenue
growth_percent
"""
)

response = client.generate_response(
    prompt
)

print(response)
SQL_GENERATION_TEMPLATE = """
You are an expert PostgreSQL analyst.

User Question:
{user_question}

Database Context:
{context}

Instructions:

1. Generate valid PostgreSQL SQL.
2. Use only tables and columns from context.
3. Do not invent columns.
4. Return SQL only.
"""
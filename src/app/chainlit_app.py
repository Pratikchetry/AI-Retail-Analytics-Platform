"""
Phase 6 — AI Retail Intelligence Platform
Chainlit Chat Interface (Premium Chat Experience).
"""

import chainlit as cl
import httpx
import pandas as pd

API_BASE = "http://localhost:8000"


@cl.on_chat_start
async def start_chat():
    """Initialize the session with a welcome message."""
    # We can just assume it's online to avoid blocking the start
    welcome_text = """# 🛍️ Retail Revenue Intelligence

Welcome to the Executive Revenue Copilot. Ask me anything about sales, customers, products, forecasts, or anomalies.

*Examples:*
- "What is the total revenue?"
- "Which country had the highest average order value?"
- "Forecast revenue for next 14 days"
- "What are the recent anomalies?"
"""
    await cl.Message(content=welcome_text).send()


@cl.on_message
async def handle_message(message: cl.Message):
    """Handle user message: call API, stream steps, format rich answer."""
    question = message.content.strip()

    # Step 1: Thinking indicator
    step = cl.Step(name="🧠 Multi-Agent System")
    await step.__aenter__()
    step.output = "Routing your question and reasoning over the warehouse..."
    await step.update()
    
    try:
        # Use async HTTP client so we DON'T freeze the Chainlit UI!
        # Set a long timeout (300s) because the agent takes time.
        async with httpx.AsyncClient(timeout=300.0) as client:
            res = await client.post(
                f"{API_BASE}/ask",
                json={"question": question}
            )
            res.raise_for_status()
            res = res.json()
            
    except Exception as e:
        step.output = f"❌ API Error: {str(e)[:100]}"
        await step.update()
        await step.__aexit__(None, None, None)
        await cl.Message(content=f"Error connecting to the backend: {e}").send()
        return

    # Close the thinking step
    step.output = "✅ Reasoning complete."
    await step.update()
    await step.__aexit__(None, None, None)

    # Step 2: Format the rich answer
    answer = res.get("answer", "No answer generated.")
    recommendation = res.get("recommendation", "")
    score = res.get("critic_score", 0.0)
    passes = res.get("critic_passes", False)
    sql = res.get("sql", "")
    route = res.get("route", "")
    evidence = res.get("evidence", "")

    md = f"## {answer}\n\n"

    if recommendation and "No action required" not in recommendation and "information not available" not in recommendation.lower():
        md += f"**🎯 Recommendation:** {recommendation}\n\n"

    status_icon = "✅" if passes else "⚠️"
    md += f"**Quality Gate:** {status_icon} Critic Score `{score:.0%}` | Route: `{route}`\n"

    await cl.Message(content=md).send()

    # Step 3: Send data visualizations if available
    result_data = res.get("result_data")
    if result_data:
        df = pd.DataFrame(result_data)
        
        elements = []
        try:
            elements.append(cl.Dataframe(name="Query Results", df=df))
        except Exception:
            pass

        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        if len(numeric_cols) > 0 and len(df) > 1:
            chart_preview = df.head(10).to_markdown(index=False)
            await cl.Message(
                content=f"**📊 Query Data:**\n```\n{chart_preview}\n```",
                elements=elements
            ).send()

    # Step 4: Show the evidence/SQL in an accordion-style step
    evidence_step = cl.Step(name="🔍 Evidence & SQL")
    await evidence_step.__aenter__()
    
    step_content = ""
    if evidence:
        step_content += f"**Evidence:**\n{evidence}\n\n"
    if sql and sql not in ("NO_SQL_REQUIRED", "INFORMATION_NOT_AVAILABLE"):
        step_content += f"**Generated SQL:**\n```sql\n{sql}\n```"
    else:
        step_content += f"**Execution Status:** {sql}"
    
    evidence_step.output = step_content
    await evidence_step.update()
    await evidence_step.__aexit__(None, None, None)
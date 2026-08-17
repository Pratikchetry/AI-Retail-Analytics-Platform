"""
Phase 1 — AI Retail Intelligence Platform
RAG Retriever Node.

Uses IntentAgent to classify, then ContextAgent to retrieve
relevant business context from ChromaDB.
"""

import os
# Prevent HuggingFace from pinging the internet on startup
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

from src.agent.intent_agent import IntentAgent
from src.agent.context_agent import ContextAgent
from src.utils.logger import get_logger
from src.langgraph.state import AgentState

log = get_logger(__name__)

# Initialize agents ONCE at the module level (when the server starts)
# This prevents reloading ChromaDB and models on every request.
_intent_agent = IntentAgent()
_context_agent = ContextAgent()

def rag_retriever_node(state: AgentState) -> dict:
    """Retrieve business context from the knowledge base."""
    question = state["question"]

    log.info("RAG retrieval for: '%s'", question[:60])

    # Reuse the cached instances
    intent = _intent_agent.classify(question)
    context_result = _context_agent.get_context(question, intent)

    context_text = ""
    if hasattr(context_result, "context"):
        context_text = context_result.context
    elif isinstance(context_result, str):
        context_text = context_result

    log.info("RAG retrieved %d chars of context", len(context_text))

    return {"context": context_text}
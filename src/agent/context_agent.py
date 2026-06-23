from dataclasses import dataclass

from src.agent.intent_agent import IntentResult

from src.rag.embedder import LocalTextEmbedder
from src.rag.index_schemas import build_and_seed_vector_warehouse
from src.rag.retriever import MetadataGroundingRetriever


@dataclass
class ContextResult:

    question: str
    domain: str
    task: str
    context: str


class ContextAgent:

    def __init__(self):

        self.embedder = LocalTextEmbedder()

        self.vector_db = (
            build_and_seed_vector_warehouse(
                None,
                self.embedder
            )
        )

        self.retriever = (
            MetadataGroundingRetriever(
                self.vector_db,
                self.embedder
            )
        )

    def _build_query(
        self,
        question,
        intent
    ):

        query = f"""
Question:
{question}

Domain:
{intent.domain}

Task:
{intent.task}
"""

        return query

    def get_context(
        self,
        question,
        intent,
        top_k=10
    ):

        query = self._build_query(
            question,
            intent
        )

        context = (
            self.retriever
            .retrieve_grounding_context(
                query,
                top_k=top_k
            )
        )

        return ContextResult(
            question=question,
            domain=intent.domain,
            task=intent.task,
            context=context
        )
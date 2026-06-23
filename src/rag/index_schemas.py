"""
Phase 5 — AI Retail Intelligence Platform
Asset-Based RAG Knowledge Warehouse Builder.
"""

from src.rag.chroma_store import ChromaVectorStore
from src.rag.embedder import LocalTextEmbedder
from src.rag.asset_loader import load_all_assets


def build_and_seed_vector_warehouse(
    executor_engine,
    embedder: LocalTextEmbedder
) -> ChromaVectorStore:

    chroma_store = ChromaVectorStore()

    documents = load_all_assets()

    contents = [
        doc["content"]
        for doc in documents
    ]

    vectors = embedder.encode_batch(
        contents
    )

    chroma_store.add_documents(
        documents,
        vectors
    )

    print(
        f"✓ Loaded {len(documents)} assets into ChromaDB"
    )

    return chroma_store
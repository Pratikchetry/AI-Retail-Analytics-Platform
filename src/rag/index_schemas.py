"""
Phase 5 — AI Retail Intelligence Platform
Asset-Based RAG Knowledge Warehouse Builder.
Cached so ChromaDB is only built and embedded ONCE per process.
"""

import functools
from src.rag.chroma_store import ChromaVectorStore
from src.rag.embedder import LocalTextEmbedder
from src.rag.asset_loader import load_all_assets


@functools.lru_cache(maxsize=1)
def get_cached_components():
    """Builds the embedder, vector store, and loads documents exactly once."""
    embedder = LocalTextEmbedder()
    chroma_store = ChromaVectorStore()
    
    # Only seed if empty to prevent duplication on restarts within same process
    if chroma_store.collection.count() == 0:
        documents = load_all_assets()
        contents = [doc["content"] for doc in documents]
        vectors = embedder.encode_batch(contents)
        chroma_store.add_documents(documents, vectors)
        print(f"✓ Seeded {len(documents)} assets into ChromaDB")
    else:
        print(f"✓ ChromaDB already populated ({chroma_store.collection.count()} assets)")
        
    return embedder, chroma_store


def build_and_seed_vector_warehouse(executor_engine, embedder_arg):
    """
    Returns the cached ChromaDB store. 
    The arguments are kept for compatibility with older agent code but are ignored.
    """
    _, chroma_store = get_cached_components()
    return chroma_store
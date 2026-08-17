"""
Phase 5 — AI Retail Intelligence Platform
ONNX Text Embedding Layer.
Uses ONNX Runtime to save 500MB of RAM (no PyTorch needed).
"""

import functools
from typing import List
from src.utils.logger import get_logger

log = get_logger(__name__)

@functools.lru_cache(maxsize=1)
def _load_onnx_model():
    """Load the ONNX model exactly once per process (uses ~30MB RAM)."""
    try:
        from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
        log.info("Loading ONNX Embedder (all-MiniLM-L6-v2)...")
        return ONNXMiniLM_L6_V2()
    except Exception as e:
        log.error(f"Failed to load ONNX model: {e}")
        raise

class LocalTextEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Model is loaded via cache
        self.model = _load_onnx_model()

    def encode_text(self, text: str) -> List[float]:
        """Encodes a single conversational string into a flat numerical vector."""
        # ChromaDB's ONNX function expects a list and returns a list of lists
        return self.model([text])[0]

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """Encodes an array of schema documentation strings in parallel."""
        return self.model(texts)
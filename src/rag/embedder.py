"""
Phase 5 — AI Retail Intelligence Platform
Localized Text Embedding Layer.
Cached to prevent reloading the model on every agent call.
"""

import os
import functools
from sentence_transformers import SentenceTransformer
from typing import List
from dotenv import load_dotenv

@functools.lru_cache(maxsize=1)
def _load_model():
    """Load the MiniLM model exactly once per process."""
    load_dotenv()
    hf_token = os.getenv("HF_TOKEN")
    if hf_token:
        os.environ["HF_TOKEN"] = hf_token
    # Silence the HF Hub warnings if no token
    os.environ["HF_HUB_OFFLINE"] = "1"
    return SentenceTransformer("all-MiniLM-L6-v2", token=hf_token)

class LocalTextEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Model is loaded via cache
        self.model = _load_model()

    def encode_text(self, text: str) -> List[float]:
        """Encodes a single conversational string into a flat numerical vector."""
        return self.model.encode(text).tolist()

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """Encodes an array of schema documentation strings in parallel."""
        return self.model.encode(texts).tolist()
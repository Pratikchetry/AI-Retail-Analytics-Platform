"""
Phase 5 — AI Retail Intelligence Platform
Localized Text Embedding Layer.
Handles 384-dimensional hardware-native vector calculations with authenticated HF Hub tracking.
"""

import os
from sentence_transformers import SentenceTransformer
from typing import List
from dotenv import load_dotenv

class LocalTextEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Explicitly pull configurations from your project_root/.env file
        load_dotenv()
        
        # Pull the authenticated token from environment parameters
        hf_token = os.getenv("HF_TOKEN")
        if hf_token:
            # Set the exact global environment flag that the huggingface_hub library looks for
            os.environ["HF_TOKEN"] = hf_token
            
        # Initialize the localized sentence transformer model safely
        self.model = SentenceTransformer(model_name, token=hf_token)

    def encode_text(self, text: str) -> List[float]:
        """Encodes a single conversational string into a flat numerical vector."""
        return self.model.encode(text).tolist()

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """Encodes an array of schema documentation strings in parallel."""
        return self.model.encode(texts).tolist()
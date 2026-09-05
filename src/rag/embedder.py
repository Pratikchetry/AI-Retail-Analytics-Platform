"""
Phase 5 — AI Retail Intelligence Platform
API-based Text Embedding Layer.
Uses Google Gemini's free Embedding API to save 500MB of RAM (no ONNX/PyTorch needed).
"""
import os
import httpx
from typing import List
from dotenv import load_dotenv
from src.utils.logger import get_logger

load_dotenv()
log = get_logger(__name__)

class LocalTextEmbedder:
    def __init__(self, model_name: str = "models/embedding-001"):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = model_name
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/{self.model}:embedContent?key={self.api_key}"
        log.info(f"Embedder initialized using Gemini API: {self.model}")

    def _call_api(self, text: str) -> List[float]:
        """Calls the Gemini API for a single string."""
        try:
            payload = {
                "model": self.model,
                "content": {"parts": [{"text": text}]}
            }
            response = httpx.post(self.api_url, json=payload, timeout=15.0)
            response.raise_for_status()
            data = response.json()
            return data.get("embedding", {}).get("values", [])
        except Exception as e:
            log.error(f"Gemini Embedding API call failed: {e}")
            raise RuntimeError(f"Gemini Embedding API failed: {e}")

    def encode_text(self, text: str) -> List[float]:
        """Encodes a single string into a vector via API."""
        return self._call_api(text)

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """Encodes an array of strings by looping."""
        results = []
        for text in texts:
            try:
                results.append(self._call_api(text))
            except Exception:
                # Fallback to empty vector if one fails to keep dimensions aligned
                results.append([0.0] * 768) 
        return results
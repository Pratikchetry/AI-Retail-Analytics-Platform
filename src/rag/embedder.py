"""
Phase 5 — AI Retail Intelligence Platform
API-based Text Embedding Layer.
Uses Hugging Face Inference API to save 500MB of RAM (no ONNX needed).
"""
import os
import time
import httpx
from typing import List
from dotenv import load_dotenv
from src.utils.logger import get_logger

load_dotenv()
log = get_logger(__name__)

class LocalTextEmbedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        self.headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
        log.info(f"Embedder initialized using HF Inference API: {model_name}")

    def _call_api(self, text: str):
        """Calls the Hugging Face API for a single string with retry logic."""
        for attempt in range(3):
            try:
                response = httpx.post(self.api_url, headers=self.headers, json={"inputs": text}, timeout=30.0)
                
                if response.status_code == 503:
                    log.warning("HF Embedding API cold booting, retrying in 5 seconds...")
                    time.sleep(5)
                    continue
                    
                # Explicitly log the error if it fails
                if response.status_code != 200:
                    log.error(f"HF API Error {response.status_code}: {response.text}")
                    response.raise_for_status()
                    
                return response.json()
                
            except Exception as e:
                log.error(f"HF Embedding API call failed: {e}")
                time.sleep(1)
                
        raise RuntimeError("Hugging Face Embedding API failed after 3 retries.")

    def encode_text(self, text: str) -> List[float]:
        """Encodes a single string into a vector via API."""
        data = self._call_api(text)
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
            return data[0]
        return data

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """Encodes an array of strings by looping to avoid payload limits."""
        results = []
        for text in texts:
            data = self._call_api(text)
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                results.append(data[0])
            else:
                results.append(data)
        return results
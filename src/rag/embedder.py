"""
Phase 5 — AI Retail Intelligence Platform
Direct ONNX Text Embedding Layer.
Bypasses ChromaDB's downloader to prevent OOM crashes on Render.
"""
import os
import numpy as np
from typing import List
from src.utils.logger import get_logger

log = get_logger(__name__)

class LocalTextEmbedder:
    def __init__(self):
        import onnxruntime
        from tokenizers import Tokenizer
        
        model_path = "/app/onnx_model/model.onnx"
        tokenizer_path = "/app/onnx_model/tokenizer.json"
        
        if not os.path.exists(model_path) or not os.path.exists(tokenizer_path):
            raise RuntimeError(f"ONNX model files not found in /app/onnx_model/. Contents: {os.listdir('/app/onnx_model/')}")
            
        self.session = onnxruntime.InferenceSession(model_path)
        self.tokenizer = Tokenizer.from_file(tokenizer_path)
        self.tokenizer.enable_padding(length=128)
        self.tokenizer.enable_truncation(max_length=128)
        log.info("Direct ONNX Embedder loaded successfully.")

    def encode_text(self, text: str) -> List[float]:
        """Encodes a single string into a vector."""
        return self._encode(text).tolist()

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """Encodes an array of strings."""
        return self._encode(texts).tolist()

    def _encode(self, texts):
        """Core ONNX inference logic."""
        if isinstance(texts, str):
            texts = [texts]
            
        encodings = self.tokenizer.encode_batch(texts)
        input_ids = np.array([e.ids for e in encodings], dtype=np.int64)
        attention_mask = np.array([e.attention_mask for e in encodings], dtype=np.int64)
        
        inputs = {
            "input_ids": input_ids,
            "attention_mask": attention_mask
        }
        
        outputs = self.session.run(None, inputs)
        # Mean pooling over token embeddings
        token_embeddings = outputs[0]
        input_mask_expanded = np.expand_dims(attention_mask, -1)
        sum_embeddings = np.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = np.clip(input_mask_expanded.sum(1), 1e-9, None)
        embeddings = sum_embeddings / sum_mask
        return embeddings[0] if len(embeddings) == 1 else embeddings
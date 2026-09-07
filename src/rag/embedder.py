"""
Phase 5 — AI Retail Intelligence Platform
Direct ONNX Text Embedding Layer.
Uses caching to ensure the model is only loaded ONCE into RAM.
"""
import os
import functools
import numpy as np
from typing import List
from src.utils.logger import get_logger

log = get_logger(__name__)

@functools.lru_cache(maxsize=1)
def _load_onnx_model():
    """Load the ONNX model exactly once per process."""
    import onnxruntime
    from tokenizers import Tokenizer
    
    possible_paths = [
        "/app/onnx_model/onnx", 
        "./onnx_model/onnx",    
        os.path.expanduser("~/.cache/chroma/onnx_models/all-MiniLM-L6-v2/onnx") 
    ]
    
    model_dir = None
    for path in possible_paths:
        if os.path.exists(os.path.join(path, "model.onnx")):
            model_dir = path
            break
            
    if not model_dir:
        raise RuntimeError(f"ONNX model files not found. Checked paths: {possible_paths}")
            
    model_path = os.path.join(model_dir, "model.onnx")
    tokenizer_path = os.path.join(model_dir, "tokenizer.json")
    
    session = onnxruntime.InferenceSession(model_path)
    tokenizer = Tokenizer.from_file(tokenizer_path)
    tokenizer.enable_padding(length=128)
    tokenizer.enable_truncation(max_length=128)
    log.info(f"Direct ONNX Embedder loaded successfully from {model_dir}")
    return session, tokenizer

class LocalTextEmbedder:
    def __init__(self):
        # This will only actually load the model the first time it is called.
        # All subsequent calls will reuse the cached session and tokenizer.
        self.session, self.tokenizer = _load_onnx_model()

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
        token_type_ids = np.array([e.type_ids for e in encodings], dtype=np.int64)
        
        inputs = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "token_type_ids": token_type_ids
        }
        
        outputs = self.session.run(None, inputs)
        token_embeddings = outputs[0]
        input_mask_expanded = np.expand_dims(attention_mask, -1)
        sum_embeddings = np.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = np.clip(input_mask_expanded.sum(1), 1e-9, None)
        embeddings = sum_embeddings / sum_mask
        
        return embeddings[0] if len(embeddings) == 1 else embeddings
"""
Phase 2 — AI Retail Intelligence Platform
Semantic Retrieval Layer: High-Performance Local Vector Store with Matrix Cosine Matching.
"""

import numpy as np
from typing import List, Dict, Any, Tuple

class LocalVectorDatabase:
    def __init__(self):
        """Initializes an isolated, zero-dependency structural index matrix array store."""
        self.vectors: List[np.ndarray] = []
        self.documents: List[Dict[str, Any]] = []

    def add_documents(self, documents: List[Dict[str, Any]], embeddings: List[list]):
        """
        Registers structural document objects alongside their calculated vector arrays.
        Each document dict must contain a 'content' field and associated tracking 'metadata'.
        """
        for doc, emb in zip(documents, embeddings):
            self.vectors.append(np.array(emb, dtype=np.float32))
            self.documents.append(doc)

    def query_similarity(self, query_embedding: list, top_k: int = 2) -> List[Tuple[Dict[str, Any], float]]:
        """
        Executes a rapid matrix dot-product to pull down highly relevant data chunks.
        Returns a sorted list of Tuples tracking (Document Object, Similarity Score).
        """
        if not self.vectors:
            return []

        # Convert structures to consolidated arrays for vector math operations
        q_v = np.array(query_embedding, dtype=np.float32)
        matrix = np.vstack(self.vectors)

        # Normalize metrics to run pure Cosine Similarity calculations safely
        q_norm = np.linalg.norm(q_v)
        matrix_norms = np.linalg.norm(matrix, axis=1)

        # Protect against division by zero errors in edge case spaces
        if q_norm == 0:
            return []
        matrix_norms = np.where(matrix_norms == 0, 1e-5, matrix_norms)

        # Compute cosine scores via normalized matrix dot products
        scores = np.dot(matrix, q_v) / (matrix_norms * q_norm)

        # Sort the index array to isolate the highest performing context frames
        ranked_indices = np.argsort(scores)[::-1][:top_k]

        return [(self.documents[idx], float(scores[idx])) for idx in ranked_indices]
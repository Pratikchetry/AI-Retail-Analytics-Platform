"""
Enterprise Chunker
Creates semantically meaningful chunks.
"""

from typing import List


class TextChunker:

    def __init__(
        self,
        chunk_size: int = 1200,
        overlap: int = 200
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(
        self,
        text: str
    ) -> List[str]:

        if not text:
            return []

        chunks = []

        start = 0

        while start < len(text):

            end = start + self.chunk_size

            chunk = text[start:end]

            chunks.append(chunk)

            start += (
                self.chunk_size
                - self.overlap
            )

        return chunks
"""
Production ChromaDB Storage Layer
"""

import chromadb


class ChromaVectorStore:

    def __init__(
        self,
        persist_directory="./chroma_store"
    ):

        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="retail_metadata_v3"
            )
        )

    def add_documents(
        self,
        documents,
        embeddings
    ):

        ids = []

        for i, doc in enumerate(documents):

            source = (
                doc["metadata"]
                .get(
                    "source_file",
                    "unknown"
                )
            )

            chunk_id = (
                doc["metadata"]
                .get(
                    "chunk_id",
                    0
                )
            )

            ids.append(
                f"{source}_{chunk_id}_{i}"
            )

        self.collection.add(
            ids=ids,
            documents=[
                d["content"]
                for d in documents
            ],
            metadatas=[
                d["metadata"]
                for d in documents
            ],
            embeddings=embeddings
        )

    def query(
        self,
        query_embedding,
        top_k=8
    ):

        return self.collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=top_k
        )
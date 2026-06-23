from typing import List
import re

class MetadataGroundingRetriever:
    def __init__(
        self,
        vector_db,
        embedder
    ):
        self.vector_db = vector_db
        self.embedder = embedder
    # =====================================================
    # Keyword Extraction
    # =====================================================
    def _extract_domain_keywords(
        self,
        query: str
    ) -> List[str]:
        query = query.lower()
        keywords = []
        important_words = re.findall(
            r"[a-zA-Z_]{3,}",
            query
        )
        stopwords = {
            "what",
            "which",
            "why",
            "how",
            "the",
            "was",
            "were",
            "did",
            "show",
            "give",
            "tell",
            "about",
            "from",
            "into",
            "with",
            "that",
            "this",
            "have",
            "has",
            "had",
            "will",
            "would",
            "should",
            "could"
        }
        for word in important_words:
            if word not in stopwords:
                keywords.append(word)
        return keywords
    # =====================================================
    # Retrieval
    # =====================================================
    def retrieve_grounding_context(
        self,
        user_query: str,
        top_k: int = 10,
        context_type: str = "mixed"
    ):
        if not user_query.strip():
            return "No query provided."
        query_vector = self.embedder.encode_text(
            user_query
        )
        results = self.vector_db.query(
            query_vector,
            top_k=25
        )
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        keywords = self._extract_domain_keywords(
            user_query
        )
        scored_docs = []
        for doc, meta in zip(
            documents,
            metadatas
        ):
            score = 0
            content_lower = doc.lower()
            collection = meta.get(
                "collection",
                ""
            )
            # =========================================
            # Keyword relevance
            # =========================================
            for keyword in keywords:
                if keyword in content_lower:
                    score += 5
            # =========================================
            # Context-aware ranking
            # =========================================
            if context_type == "schema":
                if collection == "schema_docs":
                    score += 100
                else:
                    score -= 50
            elif context_type == "business":
                if collection == "project_findings":
                    score += 100
                elif collection == "knowledge_base":
                    score += 80
                elif collection == "schema_docs":
                    score += 10
            else:
                if collection == "project_findings":
                    score += 20
                elif collection == "knowledge_base":
                    score += 10
                elif collection == "schema_docs":
                    score += 5
            scored_docs.append(
                (
                    score,
                    doc,
                    meta
                )
            )
        scored_docs.sort(
            key=lambda x: x[0],
            reverse=True
        )
        scored_docs = scored_docs[:top_k]
        # =========================================
        # Debug Output
        # =========================================
        print("\nRETRIEVAL DEBUG")
        print("=" * 80)
        for score, doc, meta in scored_docs[:5]:
            print(
                f"{meta.get('collection')} | "
                f"{meta.get('source_file')} | "
                f"score={score}"
            )
        # =========================================
        # Build Context
        # =========================================
        context_blocks = []
        for idx, (
            score,
            doc,
            meta
        ) in enumerate(
            scored_docs,
            start=1
        ):
            context_blocks.append(
                f'''

— Context Block {idx} —
Collection: {meta.get("collection")}
Domain: {meta.get("domain")}
Source: {meta.get("source_file")}
Score: {score}

{doc}
'''
            )

        return "\n".join(
            context_blocks
        )
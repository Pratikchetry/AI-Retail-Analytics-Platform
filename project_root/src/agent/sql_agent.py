from dataclasses import dataclass
import re

from src.llm.local_llm import LocalLLM

from src.agent.schema_discovery_agent import (
    SchemaDiscoveryAgent
)

from src.rag.embedder import (
    LocalTextEmbedder
)

from src.rag.index_schemas import (
    build_and_seed_vector_warehouse
)

from src.rag.retriever import (
    MetadataGroundingRetriever
)


@dataclass
class SQLGenerationResult:

    sql: str
    explanation: str
    confidence: str


class SQLAgent:

    def __init__(self):

        self.llm = LocalLLM()

        self.schema_agent = (
            SchemaDiscoveryAgent()
        )

        self.embedder = (
            LocalTextEmbedder()
        )

        self.vector_db = (
            build_and_seed_vector_warehouse(
                None,
                self.embedder
            )
        )

        self.retriever = (
            MetadataGroundingRetriever(
                self.vector_db,
                self.embedder
            )
        )

    def generate_sql(
        self,
        question: str
    ) -> SQLGenerationResult:

        schema = (
            self.schema_agent.discover()
        )

        schema_context = (
            self.retriever.retrieve_grounding_context(
                user_query=question,
                top_k=10
            )
        )

        context_lower = (
            schema_context.lower()
        )

        # =====================================
        # Metadata-only answers
        # =====================================

        metadata_keywords = [

            "superstar product",

            "cream hanging heart",

            "operationally critical month",

            "non-negotiable peak month",

            "negative yoy growth",

            "partial month effect",

            "champions segment",

            "forecast accuracy"

        ]

        for keyword in metadata_keywords:

            if keyword in context_lower:

                return SQLGenerationResult(
                    sql="NO_SQL_REQUIRED",
                    explanation="Answer already exists in metadata",
                    confidence="100"
                )

        # =====================================
        # Build column context
        # =====================================

        column_context = []

        for table, cols in schema.columns.items():

            column_context.append(
                f"""
TABLE: {table}

COLUMNS:
{", ".join(cols)}
"""
            )

        column_context = "\n".join(
            column_context
        )

        prompt = f"""
You are a Senior PostgreSQL Analytics Engineer.

QUESTION
========
{question}

AVAILABLE TABLES
================
{chr(10).join(schema.tables)}

AVAILABLE METRICS
=================
{chr(10).join(schema.metrics)}

AVAILABLE RELATIONSHIPS
=======================
{chr(10).join(schema.relationships)}

AVAILABLE COLUMNS
=================
{column_context}

RETRIEVED BUSINESS CONTEXT
==========================
{schema_context}

STRICT RULES
============

1. NEVER invent tables.

2. NEVER invent columns.

3. NEVER invent joins.

4. NEVER invent metrics.

5. ONLY use tables listed above.

6. ONLY use columns listed above.

7. ONLY use relationships listed above.

8. PostgreSQL syntax only.

9. If answer already exists inside metadata
return:

SQL:
NO_SQL_REQUIRED

10. If information is unavailable return:

SQL:
INFORMATION_NOT_AVAILABLE

11. NEVER explain inside SQL section.

12. NEVER write text after SQL.

13. SQL section must contain ONLY SQL.

14. If uncertain:
INFORMATION_NOT_AVAILABLE

Return EXACTLY:

SQL:
<query>

EXPLANATION:
<business explanation>

CONFIDENCE:
<0-100>
"""

        response = (
            self.llm.generate(prompt)
        )

        return self._parse_response(
            response
        )

    # ===================================================
    # Extract only executable SQL
    # ===================================================

    def _extract_sql_only(
        self,
        sql_text: str
    ):

        sql_text = (
            sql_text
            .replace("```sql", "")
            .replace("```", "")
        )

        sql_text = sql_text.strip()

        if (
            "NO_SQL_REQUIRED"
            in sql_text
        ):
            return "NO_SQL_REQUIRED"

        if (
            "INFORMATION_NOT_AVAILABLE"
            in sql_text
        ):
            return "INFORMATION_NOT_AVAILABLE"

        match = re.search(
            r'(SELECT|WITH).*?(;|$)',
            sql_text,
            re.IGNORECASE | re.DOTALL
        )

        if match:

            return (
                match.group(0)
                .strip()
            )

        return sql_text

    # ===================================================
    # Parse LLM Output
    # ===================================================

    def _parse_response(
        self,
        response: str
    ):

        sql = ""
        explanation = ""
        confidence = ""

        current = None

        for line in response.splitlines():

            line = line.strip()

            if line.startswith(
                "SQL:"
            ):

                current = "sql"

                value = (
                    line.replace(
                        "SQL:",
                        ""
                    )
                    .strip()
                )

                if value:
                    sql += value

                continue

            elif line.startswith(
                "EXPLANATION:"
            ):

                current = "explanation"

                value = (
                    line.replace(
                        "EXPLANATION:",
                        ""
                    )
                    .strip()
                )

                if value:
                    explanation += value

                continue

            elif line.startswith(
                "CONFIDENCE:"
            ):

                current = "confidence"

                value = (
                    line.replace(
                        "CONFIDENCE:",
                        ""
                    )
                    .strip()
                )

                if value:
                    confidence += value

                continue

            if current == "sql":

                sql += (
                    "\n" + line
                )

            elif current == "explanation":

                explanation += (
                    "\n" + line
                )

            elif current == "confidence":

                confidence += (
                    "\n" + line
                )

        sql = self._extract_sql_only(
            sql
        )

        explanation = (
            explanation.strip()
        )

        confidence = (
            confidence.strip()
        )

        if not confidence:

            confidence = "Unknown"

        return SQLGenerationResult(
            sql=sql,
            explanation=explanation,
            confidence=confidence
        )
    
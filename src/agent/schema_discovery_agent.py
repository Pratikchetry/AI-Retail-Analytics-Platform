from dataclasses import dataclass
from typing import List, Dict
import re

from src.rag.asset_loader import load_all_assets

@dataclass
class SchemaDiscoveryResult:
    tables: List[str]
    metrics: List[str]
    relationships: List[str]
    columns: Dict[str, List[str]]

class SchemaDiscoveryAgent:

    def __init__(self):
        self.documents = load_all_assets()

    def discover(self) -> SchemaDiscoveryResult:
        tables = self._extract_tables()
        metrics = self._extract_metrics()
        relationships = self._extract_relationships()
        columns = self._extract_columns()
        return SchemaDiscoveryResult(
            tables=tables,
            metrics=metrics,
            relationships=relationships,
            columns=columns
        )

    def _extract_tables(self):
        tables = set()
        for doc in self.documents:
            metadata = doc["metadata"]
            if metadata["collection"] != "schema_docs":
                continue
            content = doc["content"]
            match = re.search(
                r"table_name:\s*(.+)",
                content
            )
            if match:
                tables.add(
                    match.group(1).strip()
                )
        return sorted(list(tables))

    def _extract_metrics(self):
        metrics = set()
        for doc in self.documents:
            metadata = doc["metadata"]
            if metadata["collection"] != "metric_defs":
                continue
            content = doc["content"]
            match = re.search(
                r"metric_name:\s*(.+)",
                content
            )
            if match:
                metrics.add(
                    match.group(1).strip()
                )
        return sorted(list(metrics))

    def _extract_relationships(self):
        relationships = set()

        def normalize_relationship(rel: str):
            left, right = rel.split("=", 1)
            left = left.strip()
            right = right.strip()
            return " = ".join(
                sorted([left, right])
            )

        for doc in self.documents:
            metadata = doc["metadata"]
            if metadata["collection"] != "schema_docs":
                continue
            content = doc["content"]
            parsed = self._parse_join_patterns(
                content
            )
            for rel in parsed:
                relationships.add(
                    normalize_relationship(rel)
                )
        return sorted(
            list(relationships)
        )

    def _parse_join_patterns(
        self,
        content: str
    ):
        relationships = set()
        capture = False
        for line in content.splitlines():
            line = line.strip()
            if line.startswith(
                "join_patterns"
            ):
                capture = True
                cleaned = (
                    line.replace(
                        "join_patterns:",
                        ""
                    )
                    .replace("-", "")
                    .strip()
                )
                if "=" in cleaned:
                    relationships.add(
                        cleaned
                    )
                continue
            if capture:
                if (
                    line.startswith(
                        "business_examples"
                    )
                    or line.startswith(
                        "common_questions"
                    )
                    or line.startswith(
                        "important_columns"
                    )
                ):
                    break
                cleaned = (
                    line.replace("-", "")
                    .strip()
                )
                if "=" in cleaned:
                    relationships.add(
                        cleaned
                    )
        return relationships

    def _extract_columns(self):
        columns = {}
        for doc in self.documents:
            metadata = doc["metadata"]
            if metadata["collection"] != "schema_docs":
                continue
            content = doc["content"]
            table_match = re.search(
                r"table_name:\s*(.+)",
                content
            )
            if not table_match:
                continue
            table_name = (
                table_match.group(1)
                .strip()
                .lower()
            )
            table_columns = set()
            lines = content.splitlines()
            capture = False
            for raw in lines:
                line = raw.strip()
                if line.startswith(
                    "important_columns"
                ):
                    capture = True
                    # The asset loader places the first column on the
                    # SAME line as 'important_columns:'. Capture it here
                    # before moving on, otherwise PK/FK columns are lost.
                    if ":" in line:
                        remainder = line.split(":", 1)[1].strip()
                        # remainder looks like "country_key: Surrogate country key"
                        if ":" in remainder:
                            col = remainder.split(":")[0].strip()
                            if col and " " not in col and len(col) > 1:
                                table_columns.add(col)
                    continue
                if capture:
                    if (
                        line.startswith(
                            "join_patterns"
                        )
                        or line.startswith(
                            "business_examples"
                        )
                        or line.startswith(
                            "common_questions"
                        )
                    ):
                        break
                    if ":" in raw:
                        col = (
                            raw.split(":")[0]
                            .strip()
                        )
                        if (
                            col
                            and " " not in col
                            and len(col) > 1
                        ):
                            table_columns.add(col)
            columns[table_name] = sorted(
                list(table_columns)
            )
        return columns
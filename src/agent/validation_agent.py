from dataclasses import dataclass
import re

from src.agent.schema_discovery_agent import (
    SchemaDiscoveryAgent
)

from src.agent.business_validator import (
    BusinessValidator
)


@dataclass
class ValidationResult:
    is_valid: bool
    score: float
    errors: list
    warnings: list


class ValidationAgent:

    def __init__(self):

        schema = (
            SchemaDiscoveryAgent()
            .discover()
        )

        self.valid_tables = {
            t.lower()
            for t in schema.tables
        }

        self.valid_columns = schema.columns

        self.relationships = {
            r.lower()
            for r in schema.relationships
        }

        self.business_validator = (
            BusinessValidator()
        )

    def validate(
        self,
        sql: str,
        question: str = "",
        context: str = ""
    ):
        sql_stripped = sql.strip()
        if sql_stripped == "NO_SQL_REQUIRED":
            return ValidationResult(
                is_valid=True,
                score=100.0,
                errors=[],
                warnings=["Knowledge base answer"]
            )
        if sql_stripped == "INFORMATION_NOT_AVAILABLE":
            return ValidationResult(
                is_valid=True,
                score=100.0,
                errors=[],
                warnings=["Not in warehouse"]
            )

        errors = []
        warnings = []

        score = 100.0

        sql_lower = sql.lower()

        # -------------------------
        # SQL must start correctly
        # -------------------------

        if not sql_lower.strip().startswith(
            (
                "select",
                "with"
            )
        ):
            errors.append(
                "Only SELECT queries allowed"
            )
            score -= 30

        # -------------------------
        # Dangerous commands
        # -------------------------

        forbidden = [
            "drop ",
            "delete ",
            "update ",
            "insert ",
            "truncate ",
            "alter "
        ]

        for keyword in forbidden:

            if keyword in sql_lower:

                errors.append(
                    f"Forbidden keyword: {keyword}"
                )

                score -= 100

        # -------------------------
        # Table validation
        # -------------------------

        tables = self._extract_tables(
            sql_lower
        )

        for table in tables:

            if table not in self.valid_tables:

                errors.append(
                    f"Unknown table: {table}"
                )

                score -= 25

        # -------------------------
        # Column validation
        # -------------------------

        columns = self._extract_columns(
            sql
        )

        for table, column in columns:

            if table not in self.valid_columns:
                continue

            valid_cols = {
                c.lower()
                for c in self.valid_columns[table]
            }

            if column.lower() not in valid_cols:

                errors.append(
                    f"Unknown column: {table}.{column}"
                )

                score -= 10

        # -------------------------
        # SELECT *
        # -------------------------

        if "select *" in sql_lower:

            warnings.append(
                "Avoid SELECT *"
            )

            score -= 5

        # -------------------------
        # Business Validation Layer
        # -------------------------

        if question and context:

            business_result = (
                self.business_validator.validate(
                    question=question,
                    retrieved_context=context,
                    sql=sql
                )
            )

            if not business_result.valid:

                errors.extend(
                    business_result.errors
                )

                score -= 30

            warnings.extend(
                business_result.warnings
            )

        score = max(score, 0)

        return ValidationResult(
            is_valid=len(errors) == 0,
            score=score,
            errors=errors,
            warnings=warnings
        )

    def _extract_tables(
        self,
        sql: str
    ):

        tables = []

        patterns = [
            r'from\s+([a-zA-Z0-9_]+)',
            r'join\s+([a-zA-Z0-9_]+)'
        ]

        for pattern in patterns:

            tables.extend(
                re.findall(
                    pattern,
                    sql
                )
            )

        return tables

    def _extract_columns(
        self,
        sql: str
    ):

        columns = []

        pattern = (
            r'([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)'
        )

        matches = re.findall(
            pattern,
            sql
        )

        alias_map = self._build_alias_map(
            sql.lower()
        )

        for alias, column in matches:

            table = alias_map.get(
                alias.lower()
            )

            if table:

                columns.append(
                    (
                        table,
                        column
                    )
                )

        return columns

    def _build_alias_map(
        self,
        sql: str
    ):

        alias_map = {}

        from_matches = re.findall(
            r'from\s+([a-zA-Z0-9_]+)\s+([a-zA-Z0-9_]+)',
            sql
        )

        join_matches = re.findall(
            r'join\s+([a-zA-Z0-9_]+)\s+([a-zA-Z0-9_]+)',
            sql
        )

        for table, alias in (
            from_matches +
            join_matches
        ):
            alias_map[
                alias
            ] = table

        return alias_map
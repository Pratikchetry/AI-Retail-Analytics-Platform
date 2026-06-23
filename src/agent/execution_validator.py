from dataclasses import dataclass


@dataclass
class ExecutionValidationResult:

    valid: bool
    errors: list[str]
    warnings: list[str]


class ExecutionValidator:

    def validate(
        self,
        question: str,
        sql: str,
        execution_result
    ) -> ExecutionValidationResult:

        errors = []
        warnings = []

        q = question.lower()

        # =====================================
        # Empty result protection
        # =====================================

        if execution_result is None:

            errors.append(
                "Execution returned None."
            )

            return ExecutionValidationResult(
                valid=False,
                errors=errors,
                warnings=warnings
            )

        # =====================================
        # INFORMATION_NOT_AVAILABLE protection
        # =====================================

        if (
            "information_not_available"
            in sql.lower()
        ):

            errors.append(
                "Knowledge unavailable."
            )

        # =====================================
        # Empty dataframe/list protection
        # =====================================

        if isinstance(
            execution_result,
            list
        ):

            if len(execution_result) == 0:

                errors.append(
                    "Query returned no rows."
                )

        # =====================================
        # Customer Lifetime Value
        # =====================================

        if (
            "customer lifetime value"
            in q
            or "clv" in q
        ):

            warnings.append(
                "CLV is not currently defined in metadata."
            )

        # =====================================
        # TikTok example
        # =====================================

        if "tiktok" in q:

            errors.append(
                "Question outside warehouse scope."
            )

        return ExecutionValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
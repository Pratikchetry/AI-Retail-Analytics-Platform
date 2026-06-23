import re


class SQLValidator:

    def validate(
        self,
        user_question: str,
        sql: str
    ):

        errors = []
        warnings = []

        sql_lower = sql.lower()
        question_lower = user_question.lower()

        # BR001
        if "fact_accounting_adjustments" in sql_lower:
            if not any(
                x in question_lower
                for x in [
                    "accounting",
                    "adjustment",
                    "correction"
                ]
            ):
                errors.append(
                    "BR001 violation: accounting adjustments not requested."
                )

        # BR002
        if re.search(
            r"quantity\s*\*\s*price",
            sql_lower
        ):
            errors.append(
                "BR002 violation: revenue must use revenue column."
            )

        # BR007
        if (
            "investment_strategy" not in sql_lower
            and "case when" in sql_lower
        ):
            warnings.append(
                "Possible BR007 violation."
            )

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
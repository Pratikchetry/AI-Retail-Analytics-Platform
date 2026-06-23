from dataclasses import dataclass


@dataclass
class BusinessValidationResult:
    valid: bool
    errors: list[str]
    warnings: list[str]


class BusinessValidator:

    def validate(
        self,
        question: str,
        retrieved_context: str,
        sql: str
    ) -> BusinessValidationResult:

        errors = []
        warnings = []

        q = question.lower()
        context = retrieved_context.lower()

        # ==========================================
        # Superstar Product
        # ==========================================

        if "superstar" in q:

            required_signals = [
                "cream hanging heart",
                "only true superstar",
                "superstar product"
            ]

            if not any(
                signal in context
                for signal in required_signals
            ):
                errors.append(
                    "Required business finding missing: Superstar Product"
                )

        # ==========================================
        # Operationally Critical Month
        # ==========================================

        if "operationally critical" in q:

            required_signals = [
                "november is the non-negotiable peak month",
                "maximum load benchmark",
                "highest revenue month both years"
            ]

            if not any(
                signal in context
                for signal in required_signals
            ):
                errors.append(
                    "Required business finding missing: Operational Month"
                )

        # ==========================================
        # YoY Growth Explanation
        # ==========================================

        if (
            "negative growth" in q
            or "yoy" in q
        ):

            required_signals = [
                "partial month",
                "december 2011",
                "-0.13%",
                "first half of 2011"
            ]

            if not any(
                signal in context
                for signal in required_signals
            ):
                errors.append(
                    "Required business finding missing: YoY Explanation"
                )

        return BusinessValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
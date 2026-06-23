from dataclasses import dataclass

@dataclass
class IntentResult:
    domain: str
    task: str

class IntentAgent:

    CUSTOMER_KEYWORDS = [
        "customer",
        "customers",
        "segment",
        "segments",
        "champion",
        "champions",
        "loyal",
        "retention",
        "rfm",
        "at risk",
        "lost customer",
        "potential loyalist"
    ]
    PRODUCT_KEYWORDS = [
        "product",
        "products",
        "sku",
        "item",
        "superstar",
        "inventory"
    ]
    FORECAST_KEYWORDS = [
        "forecast",
        "future",
        "prediction",
        "predict",
        "next month",
        "next quarter"
    ]
    ANOMALY_KEYWORDS = [
    "anomaly",
    "anomalies",
    "spike",
    "spikes",
    "drop",
    "drops",
    "abnormal",
    "outlier",
    "outliers"
    ]
    REVENUE_KEYWORDS = [
        "revenue",
        "sales",
        "growth",
        "yoy",
        "month",
        "profit"
    ]
    REASONING_KEYWORDS = [
        "why",
        "reason",
        "explain",
        "root cause",
        "because"
    ]
    COMPARISON_KEYWORDS = [
        "compare",
        "comparison",
        "difference",
        "versus",
        "vs"
    ]
    FORECAST_TASK_KEYWORDS = [
        "forecast",
        "predict",
        "prediction"
    ]

    def classify(
        self,
        question: str
    ) -> IntentResult:
        q = question.lower()
        domain = self._classify_domain(q)
        task = self._classify_task(q)
        return IntentResult(
            domain=domain,
            task=task
        )

    def _contains_any(
        self,
        text: str,
        keywords: list[str]
    ) -> bool:
        return any(
            keyword in text
            for keyword in keywords
        )

    def _classify_domain(
        self,
        q: str
    ) -> str:
        # Customer first
        if self._contains_any(
            q,
            self.CUSTOMER_KEYWORDS
        ):
            return "customer"
        # Product second
        if self._contains_any(
            q,
            self.PRODUCT_KEYWORDS
        ):
            return "product"
        # Forecast third
        if self._contains_any(
            q,
            self.FORECAST_KEYWORDS
        ):
            return "forecast"
        # Anomaly fourth
        if self._contains_any(
            q,
            self.ANOMALY_KEYWORDS
        ):
            return "anomaly"
        # Revenue last
        if self._contains_any(
            q,
            self.REVENUE_KEYWORDS
        ):
            return "revenue"
        return "general"

    def _classify_task(
        self,
        q: str
    ) -> str:
        if self._contains_any(
            q,
            self.REASONING_KEYWORDS
        ):
            return "reasoning"
        if self._contains_any(
            q,
            self.COMPARISON_KEYWORDS
        ):
            return "comparison"
        if self._contains_any(
            q,
            self.FORECAST_TASK_KEYWORDS
        ):
            return "forecasting"
        return "aggregation"
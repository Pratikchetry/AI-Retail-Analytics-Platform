"""
Phase 3 — AI Retail Intelligence Platform
API request/response schemas (Pydantic).
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Any


class AskRequest(BaseModel):
    """POST /ask body."""
    question: str = Field(..., min_length=3, max_length=500)


class AskResponse(BaseModel):
    """POST /ask response."""
    question: str
    route: str
    answer: str
    recommendation: str
    evidence: str
    critic_score: float
    critic_passes: bool
    sql: Optional[str] = None
    execution_status: Optional[str] = None
    result_data: Optional[List[dict]] = None


class ForecastRequest(BaseModel):
    """POST /forecast body."""
    horizon: int = Field(default=30, ge=1, le=90)


class ForecastResponse(BaseModel):
    """POST /forecast response."""
    horizon: int
    total_revenue: float
    avg_daily_revenue: float
    days: List[dict]
    model_name: str
    model_mae: Optional[float] = None


class IngestRequest(BaseModel):
    """POST /ingest body."""
    csv_name: str = Field(default="sales_main.csv")


class IngestResponse(BaseModel):
    """POST /ingest response."""
    status: str
    rows_loaded: int
    analytics_tables_rebuilt: int


class HealthResponse(BaseModel):
    """GET /health response."""
    status: str
    database: str
    model_loaded: bool
    chroma_assets: Optional[int] = None


class MetricsResponse(BaseModel):
    """GET /metrics response."""
    total_revenue: float
    total_orders: int
    best_month: str
    best_month_revenue: float
    yoy_growth: Optional[float]
    forecast_model_mae: Optional[float]
    anomalies_detected: int
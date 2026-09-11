from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RiskInput(BaseModel):
    """Input payload for calculating business risk."""

    revenue: float = Field(..., ge=0, description="Current business revenue")
    expenses: float = Field(..., ge=0, description="Current operating expenses")
    profit: Optional[float] = Field(
        None, description="Optional current profit. Defaults to revenue - expenses."
    )
    revenue_growth: float = Field(
        0.0, description="Revenue growth percentage over previous period"
    )


class RiskResponse(BaseModel):
    """Standardized response from BizMind AI centralized RiskEngine."""

    risk_score: int = Field(
        ..., ge=0, le=100, description="Overall risk score between 0 and 100"
    )
    risk_level: str = Field(
        ..., description="Standardized risk level: Low, Medium, High, or Critical"
    )
    risk_factors: List[str] = Field(
        default_factory=list, description="Identified risk driver statements"
    )
    risk_explanation: str = Field(
        ..., description="Comprehensive explanation of business risk"
    )
    profit_margin: float = Field(..., description="Profit margin percentage")
    expense_ratio: float = Field(..., description="Operating expense ratio percentage")
    revenue_growth: float = Field(..., description="Revenue growth percentage")

from typing import List, Optional
from pydantic import BaseModel, Field


class HistoricalDataPoint(BaseModel):
    """Historical time-series record for business KPIs."""

    period: str = Field(
        ..., description="Time period label, e.g. '2026-01', 'Q1', or 'Month 1'"
    )
    revenue: float = Field(..., ge=0, description="Revenue in this period")
    expenses: float = Field(..., ge=0, description="Operating expenses in this period")
    profit: Optional[float] = Field(
        None, description="Profit in this period (defaults to revenue - expenses)"
    )
    customers: Optional[int] = Field(
        None, ge=0, description="Customer count in this period"
    )


class ForecastRequest(BaseModel):
    """Input payload for generating time-series predictive forecasts."""

    historical_data: List[HistoricalDataPoint] = Field(
        ...,
        min_length=2,
        description="At least 2 historical data periods are required for forecasting",
    )
    forecast_periods: int = Field(
        default=3, ge=1, le=24, description="Number of future periods to predict"
    )
    confidence_level: float = Field(
        default=0.90,
        ge=0.50,
        le=0.99,
        description="Confidence interval level (e.g. 0.90 for 90% confidence bands)",
    )
    include_anomaly_detection: bool = Field(
        default=True,
        description="Whether to scan historical series for anomalous outlier periods",
    )


class ForecastedDataPoint(BaseModel):
    """Predicted metrics for a single future period with confidence bands and risk score."""

    period: str
    predicted_revenue: float
    revenue_lower_bound: float
    revenue_upper_bound: float
    predicted_expenses: float
    expenses_lower_bound: float
    expenses_upper_bound: float
    predicted_profit: float
    projected_profit_margin: float
    projected_risk_score: int
    projected_risk_level: str


class TrendAnalysis(BaseModel):
    """Underlying momentum and volatility characteristics of historical data."""

    revenue_trend_direction: str
    avg_period_growth_rate: float
    expense_trend_direction: str
    volatility_score: float
    anomalies_detected: List[str] = Field(default_factory=list)


class ForecastResponse(BaseModel):
    """Comprehensive time-series forecast and predictive intelligence output."""

    forecast_horizon: int
    forecasted_periods: List[ForecastedDataPoint]
    trend_analysis: TrendAnalysis
    projected_annual_run_rate: float
    projected_future_risk_trajectory: str
    executive_takeaway: str
    confidence_score: float

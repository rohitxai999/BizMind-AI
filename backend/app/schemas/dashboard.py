from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DashboardResponse(BaseModel):
    revenue: float
    expenses: float
    profit: float

    profit_margin: float
    expense_ratio: float
    revenue_growth: float

    health_score: int
    risk_level: str

    recommendations: List[str] = Field(default_factory=list)
    risk_score: Optional[int] = None
    risk_factors: Optional[List[str]] = None
    risk_explanation: Optional[str] = None
    performance_status: Optional[str] = None
    executive_summary: Optional[str] = None


class ExecutiveDashboardResponse(BaseModel):
    revenue: float
    expenses: float
    profit: float
    profit_margin: float
    expense_ratio: float
    revenue_growth: float
    expense_growth: float
    revenue_per_employee: float
    customer_value: float
    health_score: int
    risk_score: int
    risk_level: str
    risk_factors: List[str]
    risk_explanation: str
    performance_status: str
    executive_summary: str
    recommendations: List[str] = Field(default_factory=list)
    insights: List[Dict[str, Any]] = Field(default_factory=list)
    decision_analysis: Dict[str, Any] = Field(default_factory=dict)
    opportunity_analysis: Dict[str, Any] = Field(default_factory=dict)
    executive_analysis: Dict[str, Any] = Field(default_factory=dict)
from pydantic import BaseModel
from typing import Any


class BusinessInput(BaseModel):

    revenue: float
    expenses: float
    customers: int
    employees: int

    # Previous-period revenue
    previous_revenue: float = 0


class BusinessResponse(BaseModel):

    revenue: float
    expenses: float

    profit: float

    profit_margin: float

    revenue_per_employee: float

    customer_value: float

    operating_cost_ratio: float

    business_health: int

    growth_prediction: str

    recommendations: list[str]

    # Multi-Agent Analysis
    agent_analysis: dict[str, Any]

    # Day 11 AI Business Insights
    ai_insights: dict[str, Any]

    # Day 11 Unified Executive Assessment
    unified_assessment: dict[str, Any]
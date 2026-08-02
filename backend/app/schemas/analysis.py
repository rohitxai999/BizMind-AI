from pydantic import BaseModel
from typing import Any


class BusinessInput(BaseModel):

    revenue: float
    expenses: float
    customers: int
    employees: int


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

    # NEW
    agent_analysis: dict[str, Any]
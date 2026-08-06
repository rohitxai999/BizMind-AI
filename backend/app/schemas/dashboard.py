from typing import List
from pydantic import BaseModel


class DashboardResponse(BaseModel):
    revenue: float
    expenses: float
    profit: float

    profit_margin: float
    expense_ratio: float
    revenue_growth: float

    health_score: int
    risk_level: str

    recommendations: List[str]
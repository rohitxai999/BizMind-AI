from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class BaselineBusinessInput(BaseModel):
    """Baseline metrics representing current business state."""

    revenue: float = Field(..., ge=0, description="Current baseline revenue")
    expenses: float = Field(..., ge=0, description="Current baseline expenses")
    customers: int = Field(0, ge=0, description="Current customer count")
    employees: int = Field(0, ge=0, description="Current employee headcount")
    previous_revenue: float = Field(
        0.0, ge=0, description="Revenue in the previous period"
    )
    previous_expenses: float = Field(
        0.0, ge=0, description="Expenses in the previous period"
    )


class ScenarioLevers(BaseModel):
    """Simulation levers adjusting baseline business drivers."""

    scenario_name: str = Field("Custom Scenario", description="Label for this scenario")
    revenue_change_pct: float = Field(
        0.0, description="Percentage change in revenue (e.g. +15.0 for 15% growth, -10.0 for 10% drop)"
    )
    expense_change_pct: float = Field(
        0.0, description="Percentage change in operating expenses (e.g. -10.0 for 10% cost reduction)"
    )
    customer_change_pct: float = Field(
        0.0, description="Percentage change in customer volume"
    )
    employee_change: int = Field(
        0, description="Headcount adjustment (+/- number of staff)"
    )
    description: Optional[str] = Field(
        None, description="Optional strategic rationale or hypothesis"
    )


class ScenarioSimulationInput(BaseModel):
    """Payload for running a single what-if business simulation."""

    baseline: BaselineBusinessInput
    scenario: ScenarioLevers


class ProjectedFinancials(BaseModel):
    """Financial snapshot under baseline or simulated scenario."""

    revenue: float
    expenses: float
    profit: float
    profit_margin: float
    expense_ratio: float
    revenue_growth: float
    customer_value: float
    revenue_per_employee: float
    customers: int
    employees: int


class ScenarioResult(BaseModel):
    """Complete simulation output showing impact, risk trajectory, and feasibility."""

    scenario_name: str
    description: Optional[str] = None
    baseline_financials: ProjectedFinancials
    projected_financials: ProjectedFinancials
    baseline_risk_score: int
    baseline_risk_level: str
    projected_risk_score: int
    projected_risk_level: str
    risk_delta: int
    risk_trajectory: str
    baseline_health_score: int
    projected_health_score: int
    health_delta: int
    strategic_feasibility: str
    executive_impact_summary: str
    key_takeaways: List[str]


class ScenarioComparisonInput(BaseModel):
    """Payload for comparing multiple business scenarios side by side."""

    baseline: BaselineBusinessInput
    scenarios: Optional[List[ScenarioLevers]] = Field(
        None,
        description="List of custom scenarios to evaluate. If omitted or empty, runs standard pre-packaged benchmark suite.",
    )


class ScenarioComparisonResponse(BaseModel):
    """Comparative evaluation identifying optimal business strategies."""

    baseline_financials: ProjectedFinancials
    total_scenarios: int
    results: List[ScenarioResult]
    recommended_scenario: str
    highest_profit_scenario: str
    lowest_risk_scenario: str
    executive_guidance: str

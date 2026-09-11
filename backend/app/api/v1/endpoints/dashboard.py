from fastapi import APIRouter
from app.schemas.dashboard import ExecutiveDashboardResponse
from app.services.insights_engine import InsightsEngine

router = APIRouter(prefix="/dashboard", tags=["Executive Dashboard"])


@router.get(
    "/executive-summary",
    response_model=ExecutiveDashboardResponse,
    summary="Get unified executive dashboard metrics and intelligence",
)
def executive_summary(
    revenue: float = 250000.0,
    expenses: float = 170000.0,
    previous_revenue: float = 220000.0,
    customers: int = 150,
    employees: int = 12,
):
    """
    Returns full executive intelligence suite combining KPIs,
    Centralized RiskEngine assessment, AI Insights, Decisions,
    Opportunities, and Executive Actions.
    """
    insights = InsightsEngine.generate_insights(
        revenue=revenue,
        expenses=expenses,
        previous_revenue=previous_revenue,
        customers=customers,
        employees=employees,
    )
    return ExecutiveDashboardResponse(**insights)

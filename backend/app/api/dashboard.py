from fastapi import APIRouter

from app.schemas.dashboard import DashboardResponse
from app.services.insights_engine import InsightsEngine

router = APIRouter(
    prefix="/dashboard",
    tags=["Executive Dashboard"]
)


@router.get(
    "/summary",
    response_model=DashboardResponse
)
def dashboard_summary():

    # Sample business data
    revenue = 250000
    expenses = 170000
    previous_revenue = 220000

    insights = InsightsEngine.generate_insights(
        revenue=revenue,
        expenses=expenses,
        previous_revenue=previous_revenue
    )

    return DashboardResponse(**insights)
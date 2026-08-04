from fastapi import APIRouter
from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

service = DashboardService()


@router.get("/")
def get_dashboard():
    revenue = 150000
    expenses = 90000
    previous_revenue = 130000

    profit = service.calculate_profit(revenue, expenses)
    margin = service.calculate_profit_margin(revenue, profit)
    growth = service.calculate_growth(revenue, previous_revenue)

    return {
        "revenue": revenue,
        "expenses": expenses,
        "profit": profit,
        "profit_margin": f"{margin}%",
        "growth": f"{growth}%"
    }
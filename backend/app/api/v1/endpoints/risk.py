from fastapi import APIRouter
from app.schemas.risk import RiskInput, RiskResponse
from app.services.risk.engine import RiskEngine

router = APIRouter(prefix="/risk", tags=["Risk Engine"])


@router.post(
    "/calculate",
    response_model=RiskResponse,
    summary="Calculate business risk score and identify drivers",
)
def calculate_risk(payload: RiskInput):
    """
    Direct endpoint for BizMind AI centralized Risk Engine (Day 14).
    Accepts business KPIs and produces standardized risk score, level, and drivers.
    """
    result = RiskEngine.calculate(payload.model_dump())
    return RiskResponse(**result)

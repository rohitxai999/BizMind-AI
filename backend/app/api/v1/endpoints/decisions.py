from typing import Any, Dict
from fastapi import APIRouter
from app.schemas.decision import DecisionAnalysis
from app.services.decision.engine import DecisionEngine

router = APIRouter(prefix="/decisions", tags=["Decision Engine"])
engine = DecisionEngine()


@router.post(
    "/analyze",
    response_model=DecisionAnalysis,
    summary="Generate explainable business decisions from KPIs",
)
def analyze_decisions(business_data: Dict[str, Any]):
    """
    Direct endpoint for BizMind AI Decision Engine (Day 12).
    Generates structured, evidence-backed decision cards with priorities and expected impacts.
    """
    return engine.analyze(business_data)

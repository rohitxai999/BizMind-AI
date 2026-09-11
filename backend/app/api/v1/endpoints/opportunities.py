from typing import Any, Dict
from fastapi import APIRouter
from app.schemas.opportunity import OpportunityAnalysis
from app.services.opportunity.engine import OpportunityEngine

router = APIRouter(prefix="/opportunities", tags=["Opportunity Engine"])
engine = OpportunityEngine()


@router.post(
    "/analyze",
    response_model=OpportunityAnalysis,
    summary="Identify growth and value creation opportunities",
)
def analyze_opportunities(business_data: Dict[str, Any]):
    """
    Direct endpoint for BizMind AI Opportunity Engine (Day 12).
    Discovers revenue expansion, margin expansion, and scaling opportunities.
    """
    return engine.analyze(business_data)

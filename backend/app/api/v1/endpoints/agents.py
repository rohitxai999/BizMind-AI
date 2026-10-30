from fastapi import APIRouter

from app.schemas.copilot import (
    MultiAgentSynthesisRequest,
    MultiAgentSynthesisResponse,
)
from app.services.copilot.orchestrator import MultiAgentOrchestrator

router = APIRouter(prefix="/agents", tags=["Multi-Agent System"])
orchestrator = MultiAgentOrchestrator()


@router.post(
    "/collaborate",
    response_model=MultiAgentSynthesisResponse,
    summary="Run collaborative multi-agent cross-domain assessment",
)
def collaborate(request: MultiAgentSynthesisRequest):
    """
    Direct endpoint for collaborative multi-agent intelligence.
    Executes cross-agent analysis across Finance, Sales, Marketing, Risk, and Operations,
    identifying strategic tension and consensus-driven recommendations.
    """
    return orchestrator.synthesize(request)


@router.get(
    "/list",
    summary="List available AI domain agents and their analytical scope",
)
def list_agents():
    """
    Returns registered agents in the BizMind AI multi-agent collaborative ecosystem.
    """
    return {
        "total_agents": 5,
        "agents": [
            {
                "name": "Finance Intelligence Agent",
                "domain": "finance",
                "focus": "Gross profit, net margin, burn rate, operating leverage",
                "status": "online",
            },
            {
                "name": "Sales Intelligence Agent",
                "domain": "sales",
                "focus": "Revenue per customer (ARPU), deals velocity, conversion efficiency",
                "status": "online",
            },
            {
                "name": "Marketing Intelligence Agent",
                "domain": "marketing",
                "focus": "Customer acquisition scale, market penetration, retention leverage",
                "status": "online",
            },
            {
                "name": "Risk & Compliance Agent",
                "domain": "risk",
                "focus": "Centralized RiskEngine assessment (0-100), explainable findings, mitigations",
                "status": "online",
            },
            {
                "name": "Operations & Strategy Agent",
                "domain": "operations",
                "focus": "Headcount productivity, revenue per employee, capacity scaling",
                "status": "online",
            },
        ],
    }

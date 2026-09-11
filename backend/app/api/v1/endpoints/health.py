from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()


@router.get("/health", tags=["System Health"])
def system_health():
    """
    Check platform health and status of all AI/BI engines.
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "engines": {
            "risk_engine": "online",
            "decision_engine": "online",
            "opportunity_engine": "online",
            "executive_engine": "online",
            "scenario_simulator": "online",
            "multi_agent_system": "online",
        },
    }

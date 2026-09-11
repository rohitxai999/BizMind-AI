from fastapi import APIRouter
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.risk import router as risk_router
from app.api.v1.endpoints.scenarios import router as scenarios_router
from app.api.v1.endpoints.decisions import router as decisions_router
from app.api.v1.endpoints.opportunities import router as opportunities_router
from app.api.v1.endpoints.dashboard import router as dashboard_router

api_v1_router = APIRouter()

api_v1_router.include_router(health_router)
api_v1_router.include_router(risk_router)
api_v1_router.include_router(scenarios_router)
api_v1_router.include_router(decisions_router)
api_v1_router.include_router(opportunities_router)
api_v1_router.include_router(dashboard_router)

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.agent_manager import AgentManager


router = APIRouter(
    prefix="/analysis",
    tags=["Business Analysis"]
)


manager = AgentManager()


class BusinessRequest(BaseModel):
    idea: str


@router.post("/")
async def analyze_business(request: BusinessRequest):

    report = manager.analyze_business(request.idea)

    return {
        "success": True,
        "report": report
    }
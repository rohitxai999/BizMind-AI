from fastapi import APIRouter

from app.schemas.analysis import (
    BusinessInput,
    BusinessResponse,
)

from app.services.business_service import (
    BusinessService,
)

router = APIRouter(
    prefix="/analysis",
    tags=["Business Analysis"]
)


@router.post(
    "/",
    response_model=BusinessResponse
)
def analyze_business(data: BusinessInput):
    return BusinessService.analyze(data)
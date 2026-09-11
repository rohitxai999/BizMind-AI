from fastapi import APIRouter, Query
from app.schemas.forecast import ForecastRequest, ForecastResponse
from app.services.forecast.engine import ForecastEngine

router = APIRouter(prefix="/forecast", tags=["Predictive Analytics & Forecasting"])
engine = ForecastEngine()


@router.post(
    "/predict",
    response_model=ForecastResponse,
    summary="Generate predictive forecasts for revenue, expenses, and future risk",
)
def generate_forecast(payload: ForecastRequest):
    """
    Generate forward predictive forecasts with statistical trend fitting,
    confidence intervals (prediction bands), anomaly detection, and forward
    risk evaluations via RiskEngine.
    """
    return engine.predict(payload)


@router.post(
    "/sample",
    response_model=ForecastResponse,
    summary="Generate benchmark sample forecast",
)
def generate_sample_forecast(
    periods: int = Query(
        3, ge=1, le=12, description="Number of future periods to predict"
    )
):
    """
    Convenience endpoint that executes a predictive forecast on standard
    benchmark historical time-series data.
    """
    return engine.get_sample_forecast(periods=periods)

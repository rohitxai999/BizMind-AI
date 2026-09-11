from typing import List
from fastapi import APIRouter
from app.schemas.scenario import (
    BaselineBusinessInput,
    ScenarioComparisonInput,
    ScenarioComparisonResponse,
    ScenarioLevers,
    ScenarioResult,
    ScenarioSimulationInput,
)
from app.services.simulator.engine import ScenarioSimulatorEngine

router = APIRouter(prefix="/scenarios", tags=["Business Scenario Simulator"])
simulator = ScenarioSimulatorEngine()


@router.post(
    "/simulate",
    response_model=ScenarioResult,
    summary="Simulate a what-if scenario on baseline business KPIs",
)
def simulate_scenario(payload: ScenarioSimulationInput):
    """
    Simulate strategic adjustments (revenue change, expense adjustment,
    customer scaling, hiring) against baseline metrics and project
    financials, risk shifts, and feasibility.
    """
    return simulator.simulate(payload.baseline, payload.scenario)


@router.post(
    "/compare",
    response_model=ScenarioComparisonResponse,
    summary="Compare multiple scenarios side-by-side",
)
def compare_scenarios(payload: ScenarioComparisonInput):
    """
    Simulate multiple candidate business scenarios, benchmark outcomes,
    and receive executive guidance on optimal strategy vs downside protection.
    """
    return simulator.compare_scenarios(payload.baseline, payload.scenarios)


@router.post(
    "/stress-test",
    response_model=ScenarioComparisonResponse,
    summary="Run standard stress-testing scenarios",
)
def run_stress_test(payload: BaselineBusinessInput):
    """
    Stress-test baseline metrics against standard downside economic conditions
    including Demand Recession and Cost/Supply Shocks.
    """
    return simulator.run_stress_test(payload)


@router.get(
    "/presets",
    response_model=List[ScenarioLevers],
    summary="List pre-packaged industry simulation scenarios",
)
def get_scenario_presets():
    """
    Retrieve standard pre-configured scenarios including Aggressive Expansion,
    Cost Optimization, Recession Stress Test, and Pricing Power.
    """
    return simulator.get_preset_scenarios()

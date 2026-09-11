import pytest
from app.schemas.scenario import (
    BaselineBusinessInput,
    ScenarioLevers,
)
from app.services.simulator.engine import ScenarioSimulatorEngine


@pytest.fixture
def simulator():
    return ScenarioSimulatorEngine()


@pytest.fixture
def standard_baseline():
    return BaselineBusinessInput(
        revenue=200000.0,
        expenses=120000.0,
        customers=200,
        employees=10,
        previous_revenue=180000.0,
        previous_expenses=110000.0,
    )


def test_basic_what_if_simulation(simulator, standard_baseline):
    lever = ScenarioLevers(
        scenario_name="10% Price Increase",
        revenue_change_pct=10.0,
        expense_change_pct=0.0,
        customer_change_pct=0.0,
        employee_change=0,
    )

    result = simulator.simulate(standard_baseline, lever)

    assert result.scenario_name == "10% Price Increase"
    assert result.projected_financials.revenue == 220000.0
    assert result.projected_financials.expenses == 120000.0
    assert result.projected_financials.profit == 100000.0
    assert result.projected_financials.profit_margin > result.baseline_financials.profit_margin
    assert result.strategic_feasibility in {
        "HIGHLY_RECOMMENDED",
        "VIABLE_WITH_MONITORING",
    }
    assert result.executive_impact_summary != ""
    assert len(result.key_takeaways) > 0


def test_cost_optimization_scenario_reduces_risk(simulator):
    # Baseline with borderline profitability
    baseline = BaselineBusinessInput(
        revenue=100000.0,
        expenses=85000.0,
        customers=50,
        employees=4,
        previous_revenue=100000.0,
    )

    lever = ScenarioLevers(
        scenario_name="Cost Reduction",
        revenue_change_pct=0.0,
        expense_change_pct=-20.0,
    )

    result = simulator.simulate(baseline, lever)

    assert result.projected_financials.expenses == 68000.0
    assert result.projected_financials.profit == 32000.0
    assert result.risk_delta <= 0
    assert result.risk_trajectory in {"IMPROVED", "NEUTRAL"}


def test_downside_shock_escalates_risk(simulator, standard_baseline):
    # Stress lever: severe revenue collapse and cost rise
    stress_lever = ScenarioLevers(
        scenario_name="Severe Contraction",
        revenue_change_pct=-40.0,
        expense_change_pct=15.0,
    )

    result = simulator.simulate(standard_baseline, stress_lever)

    assert result.projected_financials.profit < result.baseline_financials.profit
    assert result.risk_delta > 0
    assert result.risk_trajectory == "DETERIORATED"
    assert result.projected_risk_level in {"High", "Critical"}
    assert result.strategic_feasibility in {
        "HIGH_RISK_CAUTION",
        "CRITICAL_DOWNSIDE",
    }


def test_preset_scenarios_library(simulator):
    presets = simulator.get_preset_scenarios()
    assert len(presets) >= 4

    preset_names = [p.scenario_name for p in presets]
    assert "Aggressive Expansion" in preset_names
    assert "Recession Stress Test" in preset_names
    assert "Cost Optimization" in preset_names


def test_multi_scenario_comparison(simulator, standard_baseline):
    comparison = simulator.compare_scenarios(standard_baseline)

    assert comparison.total_scenarios >= 4
    assert comparison.recommended_scenario != ""
    assert comparison.highest_profit_scenario != ""
    assert comparison.lowest_risk_scenario != ""
    assert len(comparison.results) == comparison.total_scenarios
    assert "executive_guidance" in comparison.model_dump()


def test_run_stress_test(simulator, standard_baseline):
    stress_result = simulator.run_stress_test(standard_baseline)

    assert stress_result.total_scenarios >= 2
    for res in stress_result.results:
        assert (
            "Stress" in res.scenario_name
            or "Shock" in res.scenario_name
        )


def test_edge_case_zero_inputs(simulator):
    empty_baseline = BaselineBusinessInput(
        revenue=0.0,
        expenses=0.0,
        customers=0,
        employees=0,
    )
    lever = ScenarioLevers(scenario_name="Zero Test")

    result = simulator.simulate(empty_baseline, lever)
    assert result.projected_financials.revenue == 0.0
    assert result.projected_financials.profit == 0.0
    assert result.projected_financials.profit_margin == 0.0

import pytest

from app.schemas.copilot import CopilotQueryRequest
from app.services.copilot.engine import CopilotEngine
from app.services.copilot.repository import CopilotAuditRepository


@pytest.fixture
def copilot(tmp_path):
    db_file = str(tmp_path / "test_copilot.db")
    repo = CopilotAuditRepository(db_path=db_file)
    return CopilotEngine(repository=repo)


def test_copilot_intent_classification():
    assert (
        CopilotEngine.classify_intent("What if revenue drops by 15%?")
        == "SCENARIO_SIMULATION"
    )
    assert (
        CopilotEngine.classify_intent("Can you forecast our revenue for next quarter?")
        == "FORECAST_INQUIRY"
    )
    assert (
        CopilotEngine.classify_intent("What is our business risk score and exposure?")
        == "RISK_ANALYSIS"
    )
    assert (
        CopilotEngine.classify_intent("What strategic recommendations do the agents have?")
        == "STRATEGIC_PLANNING"
    )
    assert (
        CopilotEngine.classify_intent("Give me an executive business health diagnosis.")
        == "PERFORMANCE_DIAGNOSIS"
    )


def test_copilot_scenario_simulation_query(copilot):
    req = CopilotQueryRequest(
        query="What if our revenue drops by 20% and expenses rise by 5%?",
        business_data={
            "revenue": 200000,
            "expenses": 120000,
            "customers": 100,
            "employees": 8,
            "previous_revenue": 190000,
            "previous_expenses": 115000,
        },
    )
    res = copilot.process_query(req)

    assert res.intent == "SCENARIO_SIMULATION"
    assert "ScenarioSimulatorEngine.simulate" in res.tool_invocations
    assert "RiskEngine.calculate" in res.tool_invocations
    assert "projected_revenue" in res.data_evidence
    assert res.data_evidence["projected_revenue"] == 160000.0
    assert len(res.recommended_actions) >= 1
    assert len(res.suggested_follow_up_queries) >= 1


def test_copilot_forecast_inquiry_query(copilot):
    req = CopilotQueryRequest(
        query="Predict our future revenue and expense trajectory for the upcoming periods."
    )
    res = copilot.process_query(req)

    assert res.intent == "FORECAST_INQUIRY"
    assert "ForecastEngine.predict" in res.tool_invocations
    assert "projected_annual_run_rate" in res.data_evidence
    assert res.data_evidence["forecast_horizon"] == 3
    assert len(res.answer) > 50


def test_copilot_risk_analysis_query(copilot):
    req = CopilotQueryRequest(
        query="What is our business risk score and what factors drive it?",
        business_data={
            "revenue": 100000,
            "expenses": 85000,
            "profit": 15000,
            "revenue_growth": -5.0,
        },
    )
    res = copilot.process_query(req)

    assert res.intent == "RISK_ANALYSIS"
    assert "RiskEngine.calculate" in res.tool_invocations
    assert res.data_evidence["risk_score"] > 0
    assert "risk_level" in res.data_evidence
    assert len(res.data_evidence["risk_findings"]) >= 1


def test_copilot_strategic_planning_query(copilot):
    req = CopilotQueryRequest(
        query="What strategic action plan do you recommend to grow profitably?",
        business_data={
            "revenue": 300000,
            "expenses": 200000,
            "customers": 250,
            "employees": 15,
        },
    )
    res = copilot.process_query(req)

    assert res.intent == "STRATEGIC_PLANNING"
    assert "MultiAgentOrchestrator.synthesize" in res.tool_invocations
    assert "consensus_score" in res.data_evidence
    assert len(res.recommended_actions) >= 1


def test_copilot_audit_repository(tmp_path):
    db_file = str(tmp_path / "audit_test.db")
    repo = CopilotAuditRepository(db_path=db_file)

    # Empty initially
    assert len(repo.get_history()) == 0

    # Save interaction
    entry = repo.save_interaction(
        session_id="session-123",
        query="Test query",
        intent="RISK_ANALYSIS",
        summary="Risk is medium",
        tools_called=["RiskEngine.calculate"],
    )
    assert entry.id
    assert entry.session_id == "session-123"

    # Query history
    history = repo.get_history()
    assert len(history) == 1
    assert history[0].query == "Test query"
    assert history[0].tools_called == ["RiskEngine.calculate"]

    # Filter by session
    assert len(repo.get_history(session_id="session-123")) == 1
    assert len(repo.get_history(session_id="non-existent")) == 0

    # Clear history
    cleared = repo.clear_history()
    assert cleared == 1
    assert len(repo.get_history()) == 0

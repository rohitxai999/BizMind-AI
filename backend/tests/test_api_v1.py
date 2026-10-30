from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_v1_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "engines" in data
    assert data["engines"]["risk_engine"] == "online"
    assert data["engines"]["scenario_simulator"] == "online"
    assert data["engines"]["copilot_engine"] == "online"
    assert data["engines"]["multi_agent_orchestrator"] == "online"



def test_v1_risk_calculate():
    payload = {
        "revenue": 150000,
        "expenses": 90000,
        "revenue_growth": 12,
    }
    response = client.post("/api/v1/risk/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert "risk_level" in data
    assert data["risk_level"] in {"Low", "Medium", "High", "Critical"}
    assert data["profit_margin"] == 40.0


def test_v1_scenarios_simulate():
    payload = {
        "baseline": {
            "revenue": 100000,
            "expenses": 60000,
            "customers": 100,
            "employees": 5,
            "previous_revenue": 90000,
            "previous_expenses": 55000,
        },
        "scenario": {
            "scenario_name": "Test Expansion",
            "revenue_change_pct": 20.0,
            "expense_change_pct": 10.0,
            "customer_change_pct": 15.0,
            "employee_change": 1,
        },
    }
    response = client.post("/api/v1/scenarios/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["scenario_name"] == "Test Expansion"
    assert data["projected_financials"]["revenue"] == 120000.0
    assert data["projected_financials"]["expenses"] == 66000.0
    assert data["projected_financials"]["profit"] == 54000.0
    assert "strategic_feasibility" in data


def test_v1_scenarios_compare():
    payload = {
        "baseline": {
            "revenue": 100000,
            "expenses": 60000,
            "customers": 100,
            "employees": 5,
        }
    }
    response = client.post("/api/v1/scenarios/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_scenarios"] >= 4
    assert data["recommended_scenario"] != ""
    assert data["highest_profit_scenario"] != ""


def test_v1_scenarios_stress_test():
    payload = {
        "revenue": 100000,
        "expenses": 60000,
        "customers": 100,
        "employees": 5,
    }
    response = client.post("/api/v1/scenarios/stress-test", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_scenarios"] >= 2


def test_v1_scenarios_presets():
    response = client.get("/api/v1/scenarios/presets")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 4


def test_v1_decisions_analyze():
    payload = {
        "revenue": 100000,
        "expenses": 80000,
        "profit": 20000,
        "revenue_growth": 5,
        "expense_growth": 15,
    }
    response = client.post("/api/v1/decisions/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "decisions" in data
    assert "total_decisions" in data


def test_v1_opportunities_analyze():
    payload = {
        "revenue": 200000,
        "profit": 60000,
        "profit_margin": 30.0,
        "revenue_growth": 25.0,
        "customers": 150,
        "customer_value": 1333.33,
    }
    response = client.post("/api/v1/opportunities/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "opportunities" in data
    assert "total_opportunities" in data


def test_v1_executive_dashboard():
    response = client.get("/api/v1/dashboard/executive-summary")
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert "executive_summary" in data
    assert "decision_analysis" in data
    assert "opportunity_analysis" in data


def test_legacy_dashboard_summary_resolved():
    # Verify the bug that used to throw ValidationError is now fixed
    response = client.get("/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert "revenue" in data
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)


def test_root_and_legacy_health():
    root_resp = client.get("/")
    assert root_resp.status_code == 200
    assert "version" in root_resp.json()

    health_resp = client.get("/health")
    assert health_resp.status_code == 200
    assert health_resp.json()["status"] == "healthy"


def test_v1_forecast_predict():
    payload = {
        "historical_data": [
            {"period": "Month 1", "revenue": 100000, "expenses": 60000},
            {"period": "Month 2", "revenue": 115000, "expenses": 65000},
            {"period": "Month 3", "revenue": 130000, "expenses": 70000},
        ],
        "forecast_periods": 3,
        "confidence_level": 0.90,
    }
    response = client.post("/api/v1/forecast/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["forecast_horizon"] == 3
    assert len(data["forecasted_periods"]) == 3
    assert "projected_annual_run_rate" in data
    assert "executive_takeaway" in data
    assert data["forecasted_periods"][0]["predicted_revenue"] > 0


def test_v1_forecast_sample():
    response = client.post("/api/v1/forecast/sample?periods=4")
    assert response.status_code == 200
    data = response.json()
    assert data["forecast_horizon"] == 4
    assert len(data["forecasted_periods"]) == 4
    assert "trend_analysis" in data


def test_v1_copilot_query_scenario():
    payload = {
        "query": "What if revenue drops by 15%?",
        "business_data": {
            "revenue": 200000,
            "expenses": 140000,
            "customers": 100,
            "employees": 8,
        },
    }
    response = client.post("/api/v1/copilot/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "SCENARIO_SIMULATION"
    assert "answer" in data
    assert "projected_revenue" in data["data_evidence"]
    assert "session_id" in data


def test_v1_copilot_query_risk():
    payload = {
        "query": "What is our current risk score and financial risk level?",
        "business_data": {
            "revenue": 150000,
            "expenses": 130000,
            "profit": 20000,
            "revenue_growth": -2.0,
        },
    }
    response = client.post("/api/v1/copilot/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "RISK_ANALYSIS"
    assert "risk_score" in data["data_evidence"]


def test_v1_copilot_synthesize():
    payload = {
        "business_data": {
            "revenue": 300000,
            "expenses": 180000,
            "customers": 200,
            "employees": 10,
        }
    }
    response = client.post("/api/v1/copilot/synthesize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "consensus_score" in data
    assert len(data["perspectives"]) == 5
    assert len(data["prioritized_recommendations"]) >= 1


def test_v1_copilot_history_and_clear():
    # Make a query to populate history
    client.post(
        "/api/v1/copilot/query",
        json={"query": "Give me a company health diagnosis", "session_id": "test-session-1"},
    )

    # Get history
    hist_resp = client.get("/api/v1/copilot/history?session_id=test-session-1")
    assert hist_resp.status_code == 200
    hist_data = hist_resp.json()
    assert hist_data["total_records"] >= 1

    # Clear history
    del_resp = client.delete("/api/v1/copilot/history?session_id=test-session-1")
    assert del_resp.status_code == 200
    assert del_resp.json()["status"] == "success"


def test_v1_agents_collaborate():
    payload = {
        "business_data": {
            "revenue": 250000,
            "expenses": 150000,
            "customers": 180,
            "employees": 9,
        }
    }
    response = client.post("/api/v1/agents/collaborate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["consensus_score"] >= 0
    assert len(data["perspectives"]) == 5


def test_v1_agents_list():
    response = client.get("/api/v1/agents/list")
    assert response.status_code == 200
    data = response.json()
    assert data["total_agents"] == 5
    assert len(data["agents"]) == 5
    agent_names = [a["name"] for a in data["agents"]]
    assert "Finance Intelligence Agent" in agent_names
    assert "Risk & Compliance Agent" in agent_names



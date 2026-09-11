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


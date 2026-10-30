from app.schemas.copilot import MultiAgentSynthesisRequest
from app.services.copilot.orchestrator import MultiAgentOrchestrator


def test_orchestrator_healthy_business():
    orchestrator = MultiAgentOrchestrator()
    request = MultiAgentSynthesisRequest(
        business_data={
            "revenue": 500000,
            "expenses": 250000,
            "customers": 1200,
            "employees": 15,
            "previous_revenue": 400000,
            "previous_expenses": 230000,
            "revenue_growth": 25.0,
        }
    )

    response = orchestrator.synthesize(request)

    assert response.consensus_score >= 60
    assert response.consensus_status in {"High Alignment", "Moderate Alignment"}
    assert len(response.perspectives) == 5

    # Check all domains are represented
    domains = {p.domain for p in response.perspectives}
    assert domains == {"finance", "sales", "marketing", "risk", "operations"}

    # Check risk assessment integrated
    assert "risk_score" in response.risk_assessment
    assert response.risk_assessment["risk_score"] <= 30
    assert response.risk_assessment["risk_level"] == "Low"

    # Check explainable recommendations
    assert len(response.prioritized_recommendations) >= 2
    for rec in response.prioritized_recommendations:
        assert rec.id.startswith("REC-")
        assert rec.category
        assert rec.priority in {"Critical", "High", "Medium", "Low"}
        assert len(rec.action_plan) >= 2
        assert rec.rationale
        assert rec.timeframe
        assert rec.feasibility_score > 0


def test_orchestrator_distressed_business_debate_and_tension():
    orchestrator = MultiAgentOrchestrator()
    request = MultiAgentSynthesisRequest(
        business_data={
            "revenue": 100000,
            "expenses": 95000,
            "customers": 60,
            "employees": 12,
            "previous_revenue": 120000,
            "previous_expenses": 90000,
            "revenue_growth": -16.67,
        }
    )

    response = orchestrator.synthesize(request)

    # Risk should be critical/high
    assert response.risk_assessment["risk_score"] >= 50
    assert response.risk_assessment["risk_level"] in {"High", "Critical"}

    # Should detect debate / tension
    assert len(response.debate_points) >= 1
    capital_debate = next(
        (d for d in response.debate_points if "Capital Allocation" in d.topic),
        None,
    )
    assert capital_debate is not None
    assert "Risk & Compliance Agent" in capital_debate.dissenting_agents
    assert capital_debate.resolution != ""

    # Top recommendation must address cost optimization/risk
    top_rec = response.prioritized_recommendations[0]
    assert top_rec.category == "Cost Optimization"
    assert top_rec.priority in {"High", "Critical"}
    assert top_rec.risk_reduction_potential > 0
    assert "risk_score" in top_rec.evidence_metrics


def test_orchestrator_agent_perspectives_metrics():
    orchestrator = MultiAgentOrchestrator()
    request = MultiAgentSynthesisRequest(
        business_data={
            "revenue": 200000,
            "expenses": 100000,
            "customers": 400,
            "employees": 8,
        }
    )

    response = orchestrator.synthesize(request)

    fin_p = next(p for p in response.perspectives if p.domain == "finance")
    assert fin_p.metrics["profit"] == 100000.0
    assert fin_p.metrics["profit_margin"] == 50.0

    sales_p = next(p for p in response.perspectives if p.domain == "sales")
    assert sales_p.metrics["customers"] == 400
    assert sales_p.metrics["revenue_per_customer"] == 500.0

    ops_p = next(p for p in response.perspectives if p.domain == "operations")
    assert ops_p.metrics["revenue_per_employee"] == 25000.0

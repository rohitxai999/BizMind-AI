from app.agents.risk.agent import RiskAgent


def test_risk_agent():
    agent = RiskAgent()

    sample_data = {
        "debt": 50000,
        "cash": 100000,
    }

    result = agent.analyze(sample_data)

    assert result is not None
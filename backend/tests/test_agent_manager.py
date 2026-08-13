from app.agents.manager import AgentManager


def test_agent_manager_analyze():
    manager = AgentManager()

    sample_data = {
        "revenue": 250000,
        "expenses": 175000,
        "sales": 92,
        "sales_target": 100,
        "campaigns": 5,
        "leads": 75,
        "debt": 50000,
        "cash": 100000,
    }

    result = manager.analyze(sample_data)

    assert result is not None
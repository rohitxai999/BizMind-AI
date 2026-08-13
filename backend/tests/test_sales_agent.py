from app.agents.sales.agent import SalesAgent


def test_sales_agent():
    agent = SalesAgent()

    sample_data = {
        "sales": 92,
        "sales_target": 100,
    }

    result = agent.analyze(sample_data)

    assert result is not None
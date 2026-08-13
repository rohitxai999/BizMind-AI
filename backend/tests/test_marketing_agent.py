from app.agents.marketing.agent import MarketingAgent


def test_marketing_agent():
    agent = MarketingAgent()

    sample_data = {
        "campaigns": 5,
        "leads": 75,
    }

    result = agent.analyze(sample_data)

    assert result is not None
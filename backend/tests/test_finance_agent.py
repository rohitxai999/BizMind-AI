from app.agents.finance.agent import FinanceAgent


def test_finance_agent():
    agent = FinanceAgent()

    sample_data = {
        "revenue": 250000,
        "expenses": 175000,
    }

    result = agent.analyze(sample_data)

    assert result is not None
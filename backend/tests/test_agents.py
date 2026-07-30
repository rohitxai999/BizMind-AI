from pathlib import Path

from app.agents.finance_agent import FinanceAgent
from app.agents.strategy_agent import StrategyAgent


def test_finance_agent_returns_structured_metrics(tmp_path):
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text(
        "Product,Units_Sold,Revenue,Expenses\n"
        "Laptop,10,2000,800\n"
        "Phone,15,1800,600\n",
        encoding="utf-8",
    )

    agent = FinanceAgent()
    result = agent.analyze(str(csv_path))

    assert result["revenue"] == 3800
    assert result["profit"] == 2400
    assert result["expenses"] == 1400
    assert result["risk"] in {"Low", "Medium", "High"}


def test_strategy_agent_returns_recommendations():
    agent = StrategyAgent()
    result = agent.generate_strategy(500000, 65000, "High")

    assert isinstance(result["recommendations"], list)
    assert result["recommendations"]

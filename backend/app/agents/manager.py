from app.agents.finance.agent import FinanceAgent
from app.agents.sales.agent import SalesAgent
from app.agents.marketing.agent import MarketingAgent
from app.agents.risk.agent import RiskAgent


class AgentManager:
    """
    Coordinates all BizMind AI agents and aggregates
    their analysis into a single response.
    """

    def __init__(self):
        self.agents = [
            FinanceAgent(),
            SalesAgent(),
            MarketingAgent(),
            RiskAgent(),
        ]

    def analyze(self, data: dict) -> dict:
        results = []

        for agent in self.agents:
            try:
                results.append(agent.analyze(data))
            except Exception as e:
                results.append(
                    {
                        "agent": agent.name,
                        "status": "error",
                        "message": str(e),
                    }
                )

        return {
            "total_agents": len(self.agents),
            "results": results,
        }
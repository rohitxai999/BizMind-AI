from app.agents.base_agent import BaseAgent


class FinanceAgent(BaseAgent):
    """
    AI Agent responsible for financial analysis.
    """

    def __init__(self):
        super().__init__("Finance Agent")

    def analyze(self, data):
        revenue = data.get("revenue", 0)
        expenses = data.get("expenses", 0)

        profit = revenue - expenses

        if profit > 0:
            financial_health = "Healthy"
        elif profit == 0:
            financial_health = "Break-even"
        else:
            financial_health = "Loss"

        return {
            "agent": self.name,
            "revenue": revenue,
            "expenses": expenses,
            "profit": profit,
            "financial_health": financial_health,
            "status": "Analysis Completed"
        }
from app.agents.base_agent import BaseAgent
from app.agents.utils.logger import logger


class FinanceAgent(BaseAgent):
    """
    Finance Agent analyzes revenue, expenses,
    profit, and profit margin.
    """

    def __init__(self):
        super().__init__("Finance Agent")

    def analyze(self, data: dict) -> dict:

        logger.info(f"{self.name} started analysis")

        revenue = float(data.get("revenue", 0))
        expenses = float(data.get("expenses", 0))

        profit = revenue - expenses

        profit_margin = (
            (profit / revenue) * 100
            if revenue > 0
            else 0
        )

        if profit > 0:
            financial_health = "Healthy"
            recommendation = (
                "Business is profitable. Continue optimizing costs."
            )
        elif profit == 0:
            financial_health = "Break-even"
            recommendation = (
                "Increase revenue or reduce expenses."
            )
        else:
            financial_health = "Loss"
            recommendation = (
                "Urgent cost optimization required."
            )

        logger.info(f"{self.name} completed analysis")

        return {
            "agent": self.name,
            "status": "success",
            "revenue": revenue,
            "expenses": expenses,
            "profit": round(profit, 2),
            "profit_margin": round(profit_margin, 2),
            "financial_health": financial_health,
            "recommendation": recommendation,
        }
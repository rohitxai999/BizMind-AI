from app.agents.base_agent import BaseAgent
from app.agents.utils.logger import logger


class RiskAgent(BaseAgent):
    """
    Risk Agent evaluates business risk using
    expense ratio instead of debt/cash.
    """

    def __init__(self):
        super().__init__("Risk Agent")

    def analyze(self, data: dict) -> dict:

        logger.info(f"{self.name} started analysis")

        revenue = float(data.get("revenue", 0))
        expenses = float(data.get("expenses", 0))

        expense_ratio = (
            expenses / revenue
            if revenue > 0
            else 1
        )

        if expense_ratio <= 0.50:
            risk_level = "Low"
            recommendation = (
                "Business expenses are well controlled."
            )
        elif expense_ratio <= 0.80:
            risk_level = "Medium"
            recommendation = (
                "Monitor operating expenses carefully."
            )
        else:
            risk_level = "High"
            recommendation = (
                "Reduce expenses to improve profitability."
            )

        logger.info(f"{self.name} completed analysis")

        return {
            "agent": self.name,
            "status": "success",
            "expense_ratio": round(expense_ratio, 2),
            "risk_level": risk_level,
            "recommendation": recommendation,
        }
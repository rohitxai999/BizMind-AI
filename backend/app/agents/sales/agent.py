from app.agents.base_agent import BaseAgent
from app.agents.utils.logger import logger


class SalesAgent(BaseAgent):
    """
    Sales Agent evaluates sales performance using
    revenue generated per customer.
    """

    def __init__(self):
        super().__init__("Sales Agent")

    def analyze(self, data: dict) -> dict:

        logger.info(f"{self.name} started analysis")

        revenue = float(data.get("revenue", 0))
        customers = int(data.get("customers", 0))

        revenue_per_customer = (
            revenue / customers
            if customers > 0
            else 0
        )

        if revenue_per_customer >= 500:
            performance = "Excellent"
            recommendation = (
                "Excellent customer value. Focus on scaling sales."
            )
        elif revenue_per_customer >= 250:
            performance = "Good"
            recommendation = (
                "Sales performance is good. Improve customer retention."
            )
        elif revenue_per_customer >= 100:
            performance = "Average"
            recommendation = (
                "Increase upselling and cross-selling opportunities."
            )
        else:
            performance = "Poor"
            recommendation = (
                "Improve pricing strategy and customer acquisition."
            )

        logger.info(f"{self.name} completed analysis")

        return {
            "agent": self.name,
            "status": "success",
            "customers": customers,
            "revenue_per_customer": round(revenue_per_customer, 2),
            "performance": performance,
            "recommendation": recommendation,
        }
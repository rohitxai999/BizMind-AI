from app.agents.base_agent import BaseAgent
from app.agents.utils.logger import logger


class MarketingAgent(BaseAgent):
    """
    Marketing Agent evaluates customer growth
    and marketing effectiveness.
    """

    def __init__(self):
        super().__init__("Marketing Agent")

    def analyze(self, data: dict) -> dict:

        logger.info(f"{self.name} started analysis")

        customers = int(data.get("customers", 0))
        revenue = float(data.get("revenue", 0))

        revenue_per_customer = (
            revenue / customers
            if customers > 0
            else 0
        )

        if customers >= 1000:
            marketing_status = "Excellent Growth"
            recommendation = (
                "Customer acquisition is excellent. Scale marketing campaigns."
            )
        elif customers >= 500:
            marketing_status = "Growing"
            recommendation = (
                "Growth is steady. Focus on customer retention."
            )
        elif customers >= 100:
            marketing_status = "Stable"
            recommendation = (
                "Increase digital marketing to accelerate growth."
            )
        else:
            marketing_status = "Needs Improvement"
            recommendation = (
                "Strengthen marketing campaigns and brand awareness."
            )

        logger.info(f"{self.name} completed analysis")

        return {
            "agent": self.name,
            "status": "success",
            "customers": customers,
            "revenue_per_customer": round(revenue_per_customer, 2),
            "marketing_status": marketing_status,
            "recommendation": recommendation,
        }
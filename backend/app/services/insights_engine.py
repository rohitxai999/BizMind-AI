from typing import Dict, List


class InsightsEngine:
    """
    AI Business Insights Engine
    Calculates KPIs and business health metrics.
    """

    @staticmethod
    def generate_insights(
        revenue: float,
        expenses: float,
        previous_revenue: float
    ) -> Dict:

        profit = revenue - expenses

        # Profit Margin
        profit_margin = (
            (profit / revenue) * 100
            if revenue > 0 else 0
        )

        # Expense Ratio
        expense_ratio = (
            (expenses / revenue) * 100
            if revenue > 0 else 0
        )

        # Revenue Growth
        revenue_growth = (
            ((revenue - previous_revenue) / previous_revenue) * 100
            if previous_revenue > 0 else 0
        )

        # Business Health Score
        health_score = 100

        if profit_margin < 15:
            health_score -= 25

        if expense_ratio > 70:
            health_score -= 20

        if revenue_growth < 0:
            health_score -= 25

        health_score = max(0, min(100, health_score))

        # Risk Level
        if health_score >= 80:
            risk = "Low"
        elif health_score >= 60:
            risk = "Medium"
        else:
            risk = "High"

        recommendations: List[str] = []

        if profit_margin < 20:
            recommendations.append(
                "Increase profitability by reducing operational costs."
            )

        if expense_ratio > 65:
            recommendations.append(
                "Review major expenses and improve efficiency."
            )

        if revenue_growth < 10:
            recommendations.append(
                "Focus on sales growth and customer acquisition."
            )

        if not recommendations:
            recommendations.append(
                "Business performance is healthy. Continue monitoring KPIs."
            )

        return {
            "revenue": revenue,
            "expenses": expenses,
            "profit": profit,
            "profit_margin": round(profit_margin, 2),
            "expense_ratio": round(expense_ratio, 2),
            "revenue_growth": round(revenue_growth, 2),
            "health_score": health_score,
            "risk_level": risk,
            "recommendations": recommendations,
        }
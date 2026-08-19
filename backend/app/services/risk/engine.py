from typing import Any, Dict


class RiskEngine:
    """
    Centralized BizMind AI business risk engine.

    Produces a single explainable overall risk assessment
    from core business KPIs.
    """

    RISK_LEVELS = {
        "LOW": (0, 25),
        "MEDIUM": (26, 50),
        "HIGH": (51, 75),
        "CRITICAL": (76, 100),
    }

    @staticmethod
    def _clamp_score(score: float) -> int:
        """Keep risk score between 0 and 100."""
        return max(0, min(100, round(score)))

    @staticmethod
    def _risk_level(score: int) -> str:
        """Convert numeric risk score into a standardized level."""
        if score <= 25:
            return "Low"
        elif score <= 50:
            return "Medium"
        elif score <= 75:
            return "High"
        return "Critical"

    @staticmethod
    def calculate(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall business risk.

        Expected inputs:
        - revenue
        - expenses
        - profit
        - revenue_growth
        """

        revenue = float(data.get("revenue", 0))
        expenses = float(data.get("expenses", 0))

        profit = float(
            data.get(
                "profit",
                revenue - expenses,
            )
        )

        revenue_growth = float(
            data.get("revenue_growth", 0)
        )

        # ---------------------------------------------------------
        # Core financial metrics
        # ---------------------------------------------------------

        profit_margin = (
            (profit / revenue) * 100
            if revenue > 0
            else 0
        )

        expense_ratio = (
            (expenses / revenue) * 100
            if revenue > 0
            else 100
        )

        # ---------------------------------------------------------
        # Risk scoring
        # ---------------------------------------------------------

        risk_score = 0
        risk_factors = []

        # Profitability risk
        if profit < 0:
            risk_score += 40
            risk_factors.append(
                "Business is operating at a loss."
            )
        elif profit_margin < 10:
            risk_score += 30
            risk_factors.append(
                "Profit margin is below 10%."
            )
        elif profit_margin < 20:
            risk_score += 15
            risk_factors.append(
                "Profit margin is below 20%."
            )

        # Expense risk
        if expense_ratio > 80:
            risk_score += 30
            risk_factors.append(
                "Expenses exceed 80% of revenue."
            )
        elif expense_ratio > 70:
            risk_score += 20
            risk_factors.append(
                "Expenses exceed 70% of revenue."
            )
        elif expense_ratio > 60:
            risk_score += 10
            risk_factors.append(
                "Expenses exceed 60% of revenue."
            )

        # Growth risk
        if revenue_growth < 0:
            risk_score += 20
            risk_factors.append(
                "Revenue is declining."
            )
        elif revenue_growth < 10:
            risk_score += 10
            risk_factors.append(
                "Revenue growth is below 10%."
            )

        # ---------------------------------------------------------
        # Final score
        # ---------------------------------------------------------

        risk_score = RiskEngine._clamp_score(
            risk_score
        )

        risk_level = RiskEngine._risk_level(
            risk_score
        )

        # ---------------------------------------------------------
        # Explanation
        # ---------------------------------------------------------

        if risk_factors:
            explanation = (
                "Business risk is driven by: "
                + " ".join(risk_factors)
            )
        else:
            explanation = (
                "No major financial risk indicators "
                "were detected."
            )

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "risk_explanation": explanation,
            "profit_margin": round(profit_margin, 2),
            "expense_ratio": round(expense_ratio, 2),
            "revenue_growth": round(revenue_growth, 2),
        }
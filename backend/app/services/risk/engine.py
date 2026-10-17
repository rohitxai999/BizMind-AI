
import math
from typing import Any, Dict


class RiskEngine:
    """
    Explainable BizMind AI business risk engine.

    Scores financial risk using profitability, operating expenses,
    and revenue growth. Findings include evidence and mitigations.
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
        """Convert a numeric risk score into a standardized level."""
        if score <= 25:
            return "Low"
        if score <= 50:
            return "Medium"
        if score <= 75:
            return "High"
        return "Critical"

    @staticmethod
    def _number(data: Dict[str, Any], key: str, default=None):
        """Parse a finite numeric value or raise a useful validation error."""
        value = data.get(key, default)

        if value is None:
            if default is not None:
                return float(default)
            raise ValueError(f"Missing required risk input: '{key}'.")

        if isinstance(value, bool):
            raise ValueError(f"Risk input '{key}' must be numeric, not boolean.")

        try:
            number = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Risk input '{key}' must be a valid number."
            ) from exc

        if not math.isfinite(number):
            raise ValueError(
                f"Risk input '{key}' must be finite; NaN and infinity are invalid."
            )

        return number

    @staticmethod
    def calculate(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate an overall business risk assessment.

        Required inputs: revenue, expenses.
        Optional inputs: profit, revenue_growth.

        Existing response keys are retained. Additional fields provide
        structured findings, mitigation recommendations, and data warnings.
        """
        if not isinstance(data, dict):
            raise ValueError("Risk input must be a dictionary.")

        revenue = RiskEngine._number(data, "revenue")
        expenses = RiskEngine._number(data, "expenses")
        revenue_growth = RiskEngine._number(
            data, "revenue_growth", default=0
        )

        if revenue < 0:
            raise ValueError("Risk input 'revenue' cannot be negative.")
        if expenses < 0:
            raise ValueError("Risk input 'expenses' cannot be negative.")

        if data.get("profit") is None:
            profit = revenue - expenses
        else:
            profit = RiskEngine._number(data, "profit")

        profit_margin = (
            (profit / revenue) * 100 if revenue > 0 else 0.0
        )
        expense_ratio = (
            (expenses / revenue) * 100 if revenue > 0 else 100.0
        )

        risk_score = 0
        risk_factors = []
        risk_findings = []
        mitigation_recommendations = []
        data_quality_warnings = []

        def add_finding(
            factor,
            observed_value,
            threshold,
            severity,
            explanation,
            mitigation,
        ):
            risk_factors.append(factor)
            risk_findings.append(
                {
                    "factor": factor,
                    "observed_value": round(observed_value, 2),
                    "threshold": threshold,
                    "severity": severity,
                    "explanation": explanation,
                    "mitigation": mitigation,
                }
            )
            mitigation_recommendations.append(mitigation)

        # Profitability risk — score weights preserve existing behavior.
        if profit < 0:
            risk_score += 40
            add_finding(
                "Business is operating at a loss.",
                profit,
                "profit < 0",
                "Critical",
                "Reported or calculated profit is negative.",
                "Review major cost categories, pricing, and cash-flow "
                "requirements; develop a measurable path back to profitability.",
            )
        elif profit_margin < 10:
            risk_score += 30
            add_finding(
                "Profit margin is below 10%.",
                profit_margin,
                "profit_margin < 10%",
                "High",
                "Profit is less than 10% of revenue.",
                "Review pricing, discounts, product margins, and avoidable costs.",
            )
        elif profit_margin < 20:
            risk_score += 15
            add_finding(
                "Profit margin is below 20%.",
                profit_margin,
                "profit_margin < 20%",
                "Medium",
                "Profit margin is below the 20% monitoring threshold.",
                "Track gross and net margins and investigate material cost increases.",
            )

        # Expense risk.
        if expense_ratio > 80:
            risk_score += 30
            add_finding(
                "Expenses exceed 80% of revenue.",
                expense_ratio,
                "expense_ratio > 80%",
                "High",
                "Operating expenses consume more than 80% of revenue.",
                "Review large expense categories and identify sustainable cost reductions.",
            )
        elif expense_ratio > 70:
            risk_score += 20
            add_finding(
                "Expenses exceed 70% of revenue.",
                expense_ratio,
                "expense_ratio > 70%",
                "Medium",
                "Operating expenses consume more than 70% of revenue.",
                "Monitor expense growth against revenue and investigate cost overruns.",
            )
        elif expense_ratio > 60:
            risk_score += 10
            add_finding(
                "Expenses exceed 60% of revenue.",
                expense_ratio,
                "expense_ratio > 60%",
                "Low",
                "Operating expenses exceed the 60% monitoring threshold.",
                "Track the expense ratio each reporting period.",
            )

        # Revenue growth risk.
        if revenue_growth < 0:
            risk_score += 20
            add_finding(
                "Revenue is declining.",
                revenue_growth,
                "revenue_growth < 0%",
                "High",
                "Revenue growth is negative for the supplied period.",
                "Investigate customer churn, sales conversion, pricing changes, "
                "and seasonality before selecting corrective actions.",
            )
        elif revenue_growth < 10:
            risk_score += 10
            add_finding(
                "Revenue growth is below 10%.",
                revenue_growth,
                "revenue_growth < 10%",
                "Low",
                "Revenue growth is below the 10% monitoring threshold.",
                "Review sales pipeline, retention, and growth trends across periods.",
            )

        if revenue == 0:
            data_quality_warnings.append(
                "Revenue is zero. Profit margin and expense ratio use fallback "
                "values and may not represent meaningful financial ratios."
            )

        risk_score = RiskEngine._clamp_score(risk_score)
        risk_level = RiskEngine._risk_level(risk_score)

        if risk_factors:
            explanation = (
                "Business risk is driven by: " + " ".join(risk_factors)
            )
        else:
            explanation = (
                "No major financial risk indicators were detected by the "
                "configured profitability, expense, and growth rules."
            )

        return {
            # Existing response fields retained for compatibility.
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "risk_explanation": explanation,
            "profit_margin": round(profit_margin, 2),
            "expense_ratio": round(expense_ratio, 2),
            "revenue_growth": round(revenue_growth, 2),

            # Day 17 explainability additions.
            "risk_findings": risk_findings,
            "mitigation_recommendations": mitigation_recommendations,
            "data_quality_warnings": data_quality_warnings,
        }

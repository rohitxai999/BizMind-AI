from typing import Any, Dict, List

from app.schemas.decision import (
    BusinessDecision,
    DecisionAnalysis,
    DecisionEvidence,
)


class DecisionEngine:
    """
    Converts business metrics into structured,
    explainable business decisions.
    """

    PRIORITY_ORDER = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4,
    }

    def analyze(self, business_data: Dict[str, Any]) -> DecisionAnalysis:
        decisions: List[BusinessDecision] = []

        revenue = float(business_data.get("revenue", 0))
        expenses = float(business_data.get("expenses", 0))
        profit = float(
            business_data.get("profit", revenue - expenses)
        )

        revenue_growth = float(
            business_data.get("revenue_growth", 0)
        )

        expense_growth = float(
            business_data.get("expense_growth", 0)
        )

        profit_margin = (
            (profit / revenue) * 100
            if revenue > 0
            else 0
        )

        # 1. Expense growth analysis
        if expense_growth > revenue_growth:
            decisions.append(
                BusinessDecision(
                    title="Control Operating Expenses",
                    category="COST_OPTIMIZATION",
                    priority="HIGH",
                    problem=(
                        "Operating expenses are growing faster "
                        "than revenue."
                    ),
                    evidence=[
                        DecisionEvidence(
                            metric="Revenue Growth",
                            value=revenue_growth,
                            explanation=(
                                "Current revenue growth rate."
                            ),
                        ),
                        DecisionEvidence(
                            metric="Expense Growth",
                            value=expense_growth,
                            explanation=(
                                "Current expense growth rate."
                            ),
                        ),
                    ],
                    reasoning=(
                        "Expenses are increasing faster than revenue, "
                        "which can put pressure on future profitability."
                    ),
                    recommendation=(
                        "Review major expense categories and identify "
                        "controllable costs."
                    ),
                    expected_impact=(
                        "Improved cost efficiency and protection "
                        "of profit margins."
                    ),
                    risk_level="MEDIUM",
                    confidence=0.90,
                )
            )

        # 2. Profit margin analysis
        if 0 <= profit_margin < 10:
            decisions.append(
                BusinessDecision(
                    title="Improve Profit Margin",
                    category="PROFITABILITY",
                    priority="HIGH",
                    problem=(
                        "The business is operating with a low "
                        "profit margin."
                    ),
                    evidence=[
                        DecisionEvidence(
                            metric="Profit Margin",
                            value=round(profit_margin, 2),
                            explanation=(
                                "Current profit as a percentage "
                                "of revenue."
                            ),
                        ),
                    ],
                    reasoning=(
                        "A low profit margin provides less protection "
                        "against rising costs or declining revenue."
                    ),
                    recommendation=(
                        "Evaluate pricing, product profitability, "
                        "operating costs, and low-margin segments."
                    ),
                    expected_impact=(
                        "Higher profitability and stronger "
                        "financial resilience."
                    ),
                    risk_level="HIGH",
                    confidence=0.88,
                )
            )

        # 3. Negative profit analysis
        if profit < 0:
            decisions.append(
                BusinessDecision(
                    title="Address Negative Profit",
                    category="FINANCIAL_RISK",
                    priority="CRITICAL",
                    problem=(
                        "Business expenses are exceeding revenue."
                    ),
                    evidence=[
                        DecisionEvidence(
                            metric="Profit",
                            value=round(profit, 2),
                            explanation="Current business profit.",
                        ),
                        DecisionEvidence(
                            metric="Revenue",
                            value=round(revenue, 2),
                            explanation="Current business revenue.",
                        ),
                        DecisionEvidence(
                            metric="Expenses",
                            value=round(expenses, 2),
                            explanation="Current business expenses.",
                        ),
                    ],
                    reasoning=(
                        "Negative profit indicates that current "
                        "revenue is insufficient to cover expenses."
                    ),
                    recommendation=(
                        "Immediately review major expenses, pricing, "
                        "revenue sources, and cash-flow requirements."
                    ),
                    expected_impact=(
                        "Reduction of financial losses and movement "
                        "toward positive profitability."
                    ),
                    risk_level="CRITICAL",
                    confidence=0.98,
                )
            )

        # Sort decisions by priority
        decisions.sort(
            key=lambda decision: self.PRIORITY_ORDER.get(
                decision.priority,
                0,
            ),
            reverse=True,
        )

        critical_count = sum(
            decision.priority == "CRITICAL"
            for decision in decisions
        )

        high_count = sum(
            decision.priority == "HIGH"
            for decision in decisions
        )

        return DecisionAnalysis(
            decisions=decisions,
            total_decisions=len(decisions),
            critical_decisions=critical_count,
            high_priority_decisions=high_count,
        )
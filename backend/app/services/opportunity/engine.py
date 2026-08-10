from typing import Any, Dict, List

from app.schemas.opportunity import (
    BusinessOpportunity,
    OpportunityAnalysis,
    OpportunityEvidence,
)


class OpportunityEngine:
    """
    Identifies positive business opportunities from
    business performance metrics.
    """

    PRIORITY_ORDER = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4,
    }

    def analyze(
        self,
        business_data: Dict[str, Any],
    ) -> OpportunityAnalysis:

        opportunities: List[BusinessOpportunity] = []

        revenue = float(
            business_data.get("revenue", 0)
        )

        profit = float(
            business_data.get("profit", 0)
        )

        profit_margin = float(
            business_data.get("profit_margin", 0)
        )

        revenue_growth = float(
            business_data.get("revenue_growth", 0)
        )

        customers = int(
            business_data.get("customers", 0)
        )

        customer_value = float(
            business_data.get("customer_value", 0)
        )

        # =====================================================
        # Strong Revenue Growth Opportunity
        # =====================================================

        if revenue_growth >= 10:

            opportunities.append(
                BusinessOpportunity(
                    title="Scale Revenue Growth",
                    category="GROWTH",
                    priority="HIGH",
                    opportunity=(
                        "The business is experiencing strong "
                        "revenue growth."
                    ),
                    evidence=[
                        OpportunityEvidence(
                            metric="Revenue Growth",
                            value=revenue_growth,
                            threshold=10,
                            explanation=(
                                "Revenue growth is above the "
                                "10% growth opportunity threshold."
                            ),
                        )
                    ],
                    reasoning=(
                        "Strong revenue growth indicates that "
                        "the business may have scalable products, "
                        "channels, or customer demand."
                    ),
                    recommendation=(
                        "Identify the strongest revenue channels "
                        "and allocate additional resources to "
                        "high-performing areas."
                    ),
                    expected_impact=(
                        "Potential acceleration of revenue growth "
                        "and market expansion."
                    ),
                    confidence=0.90,
                )
            )

        # =====================================================
        # Strong Profit Margin Opportunity
        # =====================================================

        if profit_margin >= 30:

            opportunities.append(
                BusinessOpportunity(
                    title="Expand High-Margin Business",
                    category="PROFITABILITY",
                    priority="HIGH",
                    opportunity=(
                        "The business is generating a strong "
                        "profit margin."
                    ),
                    evidence=[
                        OpportunityEvidence(
                            metric="Profit Margin",
                            value=profit_margin,
                            threshold=30,
                            explanation=(
                                "Profit margin is above the "
                                "30% opportunity threshold."
                            ),
                        )
                    ],
                    reasoning=(
                        "Strong margins provide additional capacity "
                        "to reinvest in growth while maintaining "
                        "financial resilience."
                    ),
                    recommendation=(
                        "Identify the products, services, or "
                        "customer segments generating the highest "
                        "margins and consider expanding them."
                    ),
                    expected_impact=(
                        "Higher revenue and sustained profitability."
                    ),
                    confidence=0.92,
                )
            )

        # =====================================================
        # Customer Value Opportunity
        # =====================================================

        if customers > 0 and customer_value >= 500:

            opportunities.append(
                BusinessOpportunity(
                    title="Increase Customer Monetization",
                    category="CUSTOMER_GROWTH",
                    priority="MEDIUM",
                    opportunity=(
                        "Customers are generating relatively "
                        "high revenue per customer."
                    ),
                    evidence=[
                        OpportunityEvidence(
                            metric="Customer Value",
                            value=customer_value,
                            threshold=500,
                            explanation=(
                                "Average revenue per customer "
                                "is above the opportunity threshold."
                            ),
                        )
                    ],
                    reasoning=(
                        "High customer value suggests that "
                        "customers may respond well to premium "
                        "offers, upselling, or cross-selling."
                    ),
                    recommendation=(
                        "Develop premium offerings and targeted "
                        "upselling or cross-selling campaigns."
                    ),
                    expected_impact=(
                        "Higher revenue per customer and "
                        "stronger customer lifetime value."
                    ),
                    confidence=0.85,
                )
            )

        # =====================================================
        # Profitable Business Opportunity
        # =====================================================

        if profit > 0 and profit_margin >= 20:

            opportunities.append(
                BusinessOpportunity(
                    title="Reinvest Profits for Growth",
                    category="CAPITAL_ALLOCATION",
                    priority="MEDIUM",
                    opportunity=(
                        "The business is generating healthy "
                        "positive profits."
                    ),
                    evidence=[
                        OpportunityEvidence(
                            metric="Profit",
                            value=profit,
                            threshold=0,
                            explanation=(
                                "The business is currently "
                                "profitable."
                            ),
                        ),
                        OpportunityEvidence(
                            metric="Profit Margin",
                            value=profit_margin,
                            threshold=20,
                            explanation=(
                                "Profit margin is above 20%."
                            ),
                        ),
                    ],
                    reasoning=(
                        "Healthy profitability can provide "
                        "resources for strategic investments."
                    ),
                    recommendation=(
                        "Consider reinvesting a controlled portion "
                        "of profits into technology, marketing, "
                        "product development, or expansion."
                    ),
                    expected_impact=(
                        "Long-term business growth and increased "
                        "competitive advantage."
                    ),
                    confidence=0.86,
                )
            )

        # =====================================================
        # Sort Opportunities
        # =====================================================

        opportunities.sort(
            key=lambda opportunity: self.PRIORITY_ORDER.get(
                opportunity.priority,
                0,
            ),
            reverse=True,
        )

        high_priority_count = sum(
            opportunity.priority == "HIGH"
            for opportunity in opportunities
        )

        return OpportunityAnalysis(
            opportunities=opportunities,
            total_opportunities=len(opportunities),
            high_priority_opportunities=high_priority_count,
        )
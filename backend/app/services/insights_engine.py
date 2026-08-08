from typing import Dict, List


class InsightsEngine:
    """
    BizMind AI Business Insights Engine.

    Converts business KPIs into:
    - Business insights
    - Risk indicators
    - Performance signals
    - Recommendations
    """

    @staticmethod
    def generate_insights(
        revenue: float,
        expenses: float,
        previous_revenue: float = 0,
        customers: int = 0,
        employees: int = 0,
    ) -> Dict:

        # =========================================================
        # Core Financial Metrics
        # =========================================================

        profit = revenue - expenses

        profit_margin = (
            (profit / revenue) * 100
            if revenue > 0
            else 0
        )

        expense_ratio = (
            (expenses / revenue) * 100
            if revenue > 0
            else 0
        )

        revenue_growth = (
            ((revenue - previous_revenue) / previous_revenue) * 100
            if previous_revenue > 0
            else 0
        )

        revenue_per_employee = (
            revenue / employees
            if employees > 0
            else 0
        )

        customer_value = (
            revenue / customers
            if customers > 0
            else 0
        )

        # =========================================================
        # Business Health Score
        # =========================================================

        health_score = 100

        if profit_margin < 15:
            health_score -= 25
        elif profit_margin < 20:
            health_score -= 10

        if expense_ratio > 70:
            health_score -= 20
        elif expense_ratio > 60:
            health_score -= 10

        if previous_revenue > 0 and revenue_growth < 0:
            health_score -= 25
        elif previous_revenue > 0 and revenue_growth < 10:
            health_score -= 10

        if customers > 0 and customer_value < 100:
            health_score -= 10

        health_score = max(0, min(100, health_score))

        # =========================================================
        # Risk Classification
        # =========================================================

        if health_score >= 80:
            risk_level = "Low"
        elif health_score >= 60:
            risk_level = "Medium"
        else:
            risk_level = "High"

        # =========================================================
        # Business Performance Status
        # =========================================================

        if health_score >= 85:
            performance_status = "Excellent"
        elif health_score >= 70:
            performance_status = "Strong"
        elif health_score >= 50:
            performance_status = "Moderate"
        else:
            performance_status = "Weak"

        # =========================================================
        # Intelligent Insights
        # =========================================================

        insights: List[Dict] = []

        if profit_margin < 15:
            insights.append(
                {
                    "category": "Finance",
                    "severity": "Critical",
                    "title": "Low Profit Margin",
                    "finding": (
                        f"Profit margin is {round(profit_margin, 2)}%, "
                        "indicating weak profitability."
                    ),
                    "recommendation": (
                        "Reduce operating costs and review pricing strategy."
                    ),
                }
            )

        elif profit_margin < 20:
            insights.append(
                {
                    "category": "Finance",
                    "severity": "Warning",
                    "title": "Profit Margin Needs Improvement",
                    "finding": (
                        f"Profit margin is {round(profit_margin, 2)}%."
                    ),
                    "recommendation": (
                        "Look for opportunities to improve margins."
                    ),
                }
            )

        if expense_ratio > 70:
            insights.append(
                {
                    "category": "Finance",
                    "severity": "Critical",
                    "title": "High Operating Cost Ratio",
                    "finding": (
                        f"Expenses consume {round(expense_ratio, 2)}% "
                        "of revenue."
                    ),
                    "recommendation": (
                        "Review major expense categories and "
                        "identify unnecessary costs."
                    ),
                }
            )

        elif expense_ratio > 60:
            insights.append(
                {
                    "category": "Finance",
                    "severity": "Warning",
                    "title": "Elevated Operating Costs",
                    "finding": (
                        f"Operating costs represent "
                        f"{round(expense_ratio, 2)}% of revenue."
                    ),
                    "recommendation": (
                        "Monitor expenses and improve operational efficiency."
                    ),
                }
            )

        if previous_revenue > 0 and revenue_growth < 0:
            insights.append(
                {
                    "category": "Growth",
                    "severity": "Critical",
                    "title": "Revenue Decline Detected",
                    "finding": (
                        f"Revenue decreased by "
                        f"{abs(round(revenue_growth, 2))}%."
                    ),
                    "recommendation": (
                        "Investigate sales performance, customer retention "
                        "and market conditions."
                    ),
                }
            )

        elif previous_revenue > 0 and revenue_growth < 10:
            insights.append(
                {
                    "category": "Growth",
                    "severity": "Warning",
                    "title": "Slow Revenue Growth",
                    "finding": (
                        f"Revenue growth is {round(revenue_growth, 2)}%."
                    ),
                    "recommendation": (
                        "Focus on customer acquisition, retention "
                        "and sales expansion."
                    ),
                }
            )

        if employees > 0 and revenue_per_employee < 10000:
            insights.append(
                {
                    "category": "Productivity",
                    "severity": "Warning",
                    "title": "Low Revenue Per Employee",
                    "finding": (
                        f"Revenue per employee is "
                        f"{round(revenue_per_employee, 2)}."
                    ),
                    "recommendation": (
                        "Review workforce productivity and "
                        "resource allocation."
                    ),
                }
            )

        if customers > 0 and customer_value < 100:
            insights.append(
                {
                    "category": "Customers",
                    "severity": "Warning",
                    "title": "Low Customer Value",
                    "finding": (
                        f"Average revenue per customer is "
                        f"{round(customer_value, 2)}."
                    ),
                    "recommendation": (
                        "Improve customer retention, upselling "
                        "and cross-selling."
                    ),
                }
            )

        # =========================================================
        # Positive Business Signals
        # =========================================================

        if profit_margin >= 30:
            insights.append(
                {
                    "category": "Finance",
                    "severity": "Positive",
                    "title": "Strong Profitability",
                    "finding": (
                        f"Profit margin is {round(profit_margin, 2)}%, "
                        "indicating strong profitability."
                    ),
                    "recommendation": (
                        "Maintain cost discipline while exploring "
                        "controlled growth opportunities."
                    ),
                }
            )

        if previous_revenue > 0 and revenue_growth >= 10:
            insights.append(
                {
                    "category": "Growth",
                    "severity": "Positive",
                    "title": "Strong Revenue Growth",
                    "finding": (
                        f"Revenue increased by {round(revenue_growth, 2)}%."
                    ),
                    "recommendation": (
                        "Identify the drivers of growth and scale "
                        "high-performing channels."
                    ),
                }
            )

        # =========================================================
        # Default Insight
        # =========================================================

        if not insights:
            insights.append(
                {
                    "category": "Overall",
                    "severity": "Positive",
                    "title": "Business Performance Stable",
                    "finding": (
                        "No major negative business signals were detected."
                    ),
                    "recommendation": (
                        "Continue monitoring KPIs and business trends."
                    ),
                }
            )

        # =========================================================
        # Executive Summary
        # =========================================================

        executive_summary = (
            f"Business performance is {performance_status.lower()} "
            f"with a health score of {health_score}/100. "
            f"Current risk level is {risk_level.lower()}."
        )

        # =========================================================
        # Final Result
        # =========================================================

        return {
            "revenue": round(revenue, 2),
            "expenses": round(expenses, 2),
            "profit": round(profit, 2),
            "profit_margin": round(profit_margin, 2),
            "expense_ratio": round(expense_ratio, 2),
            "revenue_growth": round(revenue_growth, 2),
            "revenue_per_employee": round(
                revenue_per_employee,
                2
            ),
            "customer_value": round(
                customer_value,
                2
            ),
            "health_score": health_score,
            "risk_level": risk_level,
            "performance_status": performance_status,
            "executive_summary": executive_summary,
            "insights": insights,
        }
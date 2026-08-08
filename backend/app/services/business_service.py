from app.agents.manager import AgentManager
from app.services.insights_engine import InsightsEngine
from app.services.assessment.engine import UnifiedAssessmentEngine


class BusinessService:

    @staticmethod
    def analyze(data):

        revenue = data.revenue
        expenses = data.expenses
        customers = data.customers
        employees = data.employees
        previous_revenue = data.previous_revenue

        # =========================================================
        # Core KPI Analysis
        # =========================================================

        profit = revenue - expenses

        profit_margin = (
            (profit / revenue) * 100
            if revenue > 0 else 0
        )

        revenue_per_employee = (
            revenue / employees
            if employees > 0 else 0
        )

        customer_value = (
            revenue / customers
            if customers > 0 else 0
        )

        operating_cost_ratio = (
            (expenses / revenue) * 100
            if revenue > 0 else 0
        )

        # =========================================================
        # AI Business Insights Engine
        # =========================================================

        insights = InsightsEngine.generate_insights(
            revenue=revenue,
            expenses=expenses,
            previous_revenue=previous_revenue,
            customers=customers,
            employees=employees
        )

        # =========================================================
        # Business Health
        # =========================================================

        health = insights["health_score"]

        if health >= 85:
            growth = "Excellent"
        elif health >= 70:
            growth = "Strong"
        elif health >= 55:
            growth = "Moderate"
        else:
            growth = "Weak"

        # =========================================================
        # Recommendations
        # =========================================================

        recommendations = [
            insight["recommendation"]
            for insight in insights["insights"]
        ]

        # Remove duplicates
        recommendations = list(
            dict.fromkeys(recommendations)
        )

        # =========================================================
        # Multi-Agent Analysis
        # =========================================================

        manager = AgentManager()

        agent_analysis = manager.analyze(
            {
                "revenue": revenue,
                "expenses": expenses,
                "customers": customers,
                "employees": employees,
                "previous_revenue": previous_revenue,
            }
        )

        # =========================================================
        # Unified Executive Assessment
        # =========================================================

        unified_assessment = (
            UnifiedAssessmentEngine.generate_assessment(
                insights=insights,
                agent_analysis=agent_analysis
            )
        )

        # =========================================================
        # Final Response
        # =========================================================

        return {
            "revenue": revenue,
            "expenses": expenses,

            "profit": round(
                profit,
                2
            ),

            "profit_margin": round(
                profit_margin,
                2
            ),

            "revenue_per_employee": round(
                revenue_per_employee,
                2
            ),

            "customer_value": round(
                customer_value,
                2
            ),

            "operating_cost_ratio": round(
                operating_cost_ratio,
                2
            ),

            "business_health": health,

            "growth_prediction": growth,

            "recommendations": recommendations,

            # Multi-Agent Analysis
            "agent_analysis": agent_analysis,

            # Day 11 AI Insights
            "ai_insights": insights,

            # Day 11 Unified Assessment
            "unified_assessment": unified_assessment,
        }
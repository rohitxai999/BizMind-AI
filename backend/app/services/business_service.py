from app.agents.manager import AgentManager


class BusinessService:

    @staticmethod
    def analyze(data):

        revenue = data.revenue
        expenses = data.expenses
        customers = data.customers
        employees = data.employees

        # ==========================
        # Core KPI Analysis
        # ==========================

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

        health = 50

        if profit_margin >= 30:
            health += 20

        if revenue_per_employee >= 10000:
            health += 10

        if customer_value >= 100:
            health += 10

        if operating_cost_ratio <= 60:
            health += 10

        health = min(100, health)

        if health >= 85:
            growth = "Excellent"
        elif health >= 70:
            growth = "Strong"
        elif health >= 55:
            growth = "Moderate"
        else:
            growth = "Weak"

        recommendations = []

        if profit_margin < 20:
            recommendations.append(
                "Reduce operating expenses."
            )

        if operating_cost_ratio > 70:
            recommendations.append(
                "High operating costs detected."
            )

        if revenue_per_employee < 10000:
            recommendations.append(
                "Improve employee productivity."
            )

        if customer_value < 100:
            recommendations.append(
                "Increase average customer value."
            )

        if not recommendations:
            recommendations.append(
                "Business performance is excellent."
            )

        # ==========================
        # Multi-Agent Analysis
        # ==========================

        manager = AgentManager()

        agent_analysis = manager.analyze({
            "revenue": revenue,
            "expenses": expenses,
            "customers": customers,
            "employees": employees
        })

        # ==========================
        # Final Response
        # ==========================

        return {

            "revenue": revenue,
            "expenses": expenses,

            "profit": round(profit, 2),

            "profit_margin": round(
                profit_margin, 2
            ),

            "revenue_per_employee": round(
                revenue_per_employee, 2
            ),

            "customer_value": round(
                customer_value, 2
            ),

            "operating_cost_ratio": round(
                operating_cost_ratio, 2
            ),

            "business_health": health,

            "growth_prediction": growth,

            "recommendations": recommendations,

            "agent_analysis": agent_analysis
        }
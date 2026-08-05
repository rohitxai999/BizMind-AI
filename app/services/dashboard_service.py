class DashboardService:

    def calculate_profit(self, revenue: float, expenses: float):
        return revenue - expenses

    def calculate_profit_margin(self, revenue: float, profit: float):
        if revenue == 0:
            return 0
        return round((profit / revenue) * 100, 2)

    def calculate_growth(self, current: float, previous: float):
        if previous == 0:
            return 0
        return round(((current - previous) / previous) * 100, 2)

    def business_health(self, margin: float):
        if margin >= 30:
            return "Excellent"
        elif margin >= 20:
            return "Good"
        elif margin >= 10:
            return "Average"
        else:
            return "Needs Improvement"

    def health_score(self, margin: float):
        if margin >= 30:
            return 100
        elif margin >= 20:
            return 80
        elif margin >= 10:
            return 60
        else:
            return 40

    def monthly_trends(self):
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun"
        ]

        revenue = [
            100000,
            110000,
            120000,
            130000,
            145000,
            150000
        ]

        expenses = [
            70000,
            75000,
            80000,
            82000,
            87000,
            90000
        ]

        profit = [
            revenue[i] - expenses[i]
            for i in range(len(months))
        ]

        return {
            "months": months,
            "revenue": revenue,
            "expenses": expenses,
            "profit": profit
        }

    def executive_summary(self):
        return [
            "Revenue is steadily increasing.",
            "Profit margin is above target.",
            "Operating expenses remain under control.",
            "Business health is excellent."
        ]
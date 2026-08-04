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
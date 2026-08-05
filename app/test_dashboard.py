from app.services.dashboard_service import DashboardService

service = DashboardService()

revenue = 150000
expenses = 90000
previous_revenue = 130000

profit = service.calculate_profit(revenue, expenses)
margin = service.calculate_margin(revenue, expenses)
growth = service.calculate_growth(previous_revenue, revenue)
health = service.business_health(margin)
score = service.health_score(margin)

print("=" * 40)
print("BizMind AI Dashboard Test")
print("=" * 40)
print("Revenue:", revenue)
print("Expenses:", expenses)
print("Profit:", profit)
print("Profit Margin:", margin, "%")
print("Revenue Growth:", growth, "%")
print("Business Health:", health)
print("Health Score:", score)
class AnalyticsAgent:


    def analyze(self, data):

        total_revenue = 0
        total_expenses = 0
        total_customers = 0


        for item in data:

            total_revenue += item["revenue"]
            total_expenses += item["expenses"]
            total_customers += item["customers"]


        profit = total_revenue - total_expenses


        return {

            "total_revenue": total_revenue,
            "total_expenses": total_expenses,
            "profit": profit,
            "customers": total_customers,
            "months_analyzed": len(data)

        }
class HealthAgent:

    def calculate(self, revenue, profit, expenses, risk):

        score = 100

        if profit < revenue * 0.20:
            score -= 20

        if expenses > revenue * 0.70:
            score -= 20

        if risk == "High":
            score -= 30
        elif risk == "Medium":
            score -= 15

        score = max(0, min(100, score))

        if score >= 85:
            status = "Excellent"

        elif score >= 70:
            status = "Good"

        elif score >= 50:
            status = "Average"

        else:
            status = "Poor"

        return {
            "score": score,
            "status": status
        }
class StrategyAgent:
    def generate_strategy(self, revenue, profit, risk):
        recommendations = []

        if risk == "High":
            recommendations.append("Protect cash flow and reduce unnecessary spending immediately.")

        if profit < revenue * 0.2:
            recommendations.append("Focus on higher-margin products and tighten pricing discipline.")

        if revenue < 100000:
            recommendations.append("Increase targeted marketing on the strongest-performing channels.")

        recommendations.append("Improve customer retention with loyalty and service programs.")
        recommendations.append("Automate repeatable workflows to improve operating efficiency.")

        if not recommendations:
            recommendations.append("Maintain the current growth momentum and monitor key KPIs weekly.")

        return {
            "recommendations": recommendations[:5]
        }
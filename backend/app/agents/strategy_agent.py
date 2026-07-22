class StrategyAgent:


    def generate_strategy(
        self,
        revenue,
        profit,
        risk
    ):


        recommendations = []


        if profit < revenue * 0.2:
            recommendations.append(
                "Improve profit margin by reducing costs"
            )


        if risk == "High":
            recommendations.append(
                "Review expenses and cash flow"
            )


        else:
            recommendations.append(
                "Increase investment in growth areas"
            )


        recommendations.append(
            "Analyze customer demand before expanding"
        )


        return {

            "business_status": risk,

            "recommendations": recommendations,

            "message":
            "Strategy generated successfully 🚀"
        }
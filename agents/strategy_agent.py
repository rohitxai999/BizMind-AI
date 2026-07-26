class StrategyAgent:


    def generate_strategy(self, report):

        strategies = []


        if "Slow growth" in report.values():
            strategies.append(
                "Improve marketing and customer acquisition"
            )


        if report["profit"] < 50000:
            strategies.append(
                "Reduce operational expenses"
            )


        strategies.append(
            "Focus on customer retention"
        )


        return strategies
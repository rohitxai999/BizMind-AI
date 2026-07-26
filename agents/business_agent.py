class BusinessAgent:


    def analyze_business(self, metrics):

        report = {}


        if metrics["profit"] > 0:
            report["status"] = "Business is profitable"
        else:
            report["status"] = "Business needs improvement"



        average_revenue = (
            metrics["total_revenue"] /
            metrics["months_analyzed"]
        )


        if average_revenue > 150000:
            report["growth"] = "Strong revenue performance"
        else:
            report["growth"] = "Revenue growth can improve"



        report["profit"] = metrics["profit"]

        report["customers"] = metrics["customers"]


        return report
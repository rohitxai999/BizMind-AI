import pandas as pd


class FinanceAgent:

    def analyze(self, file_path):

        df = pd.read_csv(file_path)

        revenue = df["Revenue"].sum()

        expenses = df["Expenses"].sum()

        profit = revenue - expenses

        margin = (profit / revenue) * 100


        if margin < 20:
            risk = "High"
        elif margin < 50:
            risk = "Medium"
        else:
            risk = "Low"


        return {
            "revenue": int(revenue),
            "expenses": int(expenses),
            "profit": int(profit),
            "profit_margin": round(margin, 2),
            "risk": risk
        }
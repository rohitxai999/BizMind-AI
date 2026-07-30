import pandas as pd


class FinanceAgent:
    def analyze(self, file_path: str):
        df = pd.read_csv(file_path)

        if df.empty:
            return {
                "error": "CSV file is empty"
            }

        required_columns = ["Revenue", "Expenses"]
        missing_columns = [column for column in required_columns if column not in df.columns]

        if missing_columns:
            return {
                "error": f"Missing column(s): {', '.join(missing_columns)}"
            }

        revenue = float(df["Revenue"].sum())
        expenses = float(df["Expenses"].sum())
        profit = revenue - expenses

        if revenue > 0:
            expense_ratio = (expenses / revenue) * 100
            profit_margin = (profit / revenue) * 100
        else:
            expense_ratio = 0.0
            profit_margin = 0.0

        if expense_ratio > 70 or profit_margin < 5:
            risk = "High"
        elif expense_ratio > 50 or profit_margin < 15:
            risk = "Medium"
        else:
            risk = "Low"

        return {
            "revenue": int(revenue),
            "profit": int(profit),
            "expenses": int(expenses),
            "risk": risk,
            "profit_margin": round(profit_margin, 2),
            "expense_ratio": round(expense_ratio, 2),
        }
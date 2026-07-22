import pandas as pd


class DataAnalystAgent:

    def analyze(self, file_path):

        df = pd.read_csv(file_path)

        if df.empty:
            return {
                "error": "CSV file is empty"
            }

        # Check required columns
        required_columns = [
            "Product",
            "Units_Sold",
            "Revenue",
            "Expenses"
        ]

        for column in required_columns:
            if column not in df.columns:
                return {
                    "error": f"Missing column: {column}"
                }

        total_sales = df["Units_Sold"].sum()

        total_revenue = df["Revenue"].sum()

        best_product = df.loc[
            df["Revenue"].idxmax(),
            "Product"
        ]

        return {
            "total_sales": int(total_sales),
            "total_revenue": int(total_revenue),
            "best_product": best_product,
            "insight": "Business data analyzed successfully 🚀"
        }
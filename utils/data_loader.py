import csv


class DataLoader:


    def load_business_data(self, file_path):

        data = []


        with open(file_path, "r") as file:

            reader = csv.DictReader(file)

            for row in reader:

                data.append({

                    "month": row["month"],
                    "revenue": int(row["revenue"]),
                    "expenses": int(row["expenses"]),
                    "customers": int(row["customers"])

                })


        return data
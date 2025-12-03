import csv

class CSV_Creater:
    def __init__(self, csv_path=str):
        self.csv_path = csv_path

    def create_csv(self, data, output_csv_path):


        with open(output_csv_path, "w", encoding="utf-8") as f:
            f.write(data)



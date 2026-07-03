import pandas as pd
from pathlib import Path


class WeightedStrategy:

    def __init__(self, old_csv, new_csv):
        self.old_df = pd.read_csv(old_csv)
        self.new_df = pd.read_csv(new_csv)

    def update_weight(self, old_weight, new_weight):

        self.total_rows = len(self.old_df)
        print("Total Rows", self.total_rows)
        print("Len of old df ", len(self.old_df))

        self.old_rows = int(self.total_rows * old_weight)
        self.new_rows = int(self.total_rows - self.old_rows)
        print("Old Rows", self.old_rows)

        self.old_data = self.old_df.sample(n=self.old_rows)
        self.new_data = self.new_df.sample(n=self.new_rows)
        self.updated_weights = pd.concat([self.old_data, self.new_data])

        return self.updated_weights

    def save_updated_df(self, filename):
        self.updated_weights.to_csv(filename, index=False)


org_df = Path("Task_3\\data\\weather_data.csv")
current_df = Path("Task_3\\data\\weather_drifted_data.csv")
updater = WeightedStrategy(org_df, current_df)
updated_df = updater.update_weight(0.3, 0.7)
print(updated_df)
updater.save_updated_df("Task_3\\data\\updated_weather_data.csv")

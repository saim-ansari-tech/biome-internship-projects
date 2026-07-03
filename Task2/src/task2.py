import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


class DataDrift:
    def __init__(self, baseline_csv, current_csv):
        self.baseline_df = pd.read_csv(baseline_csv)
        self.current_df = pd.read_csv(current_csv)

    def calculate_psi(self, expected, actual, bins=10):
        breakpoints = np.percentile(expected, np.linspace(0, 100, bins + 1))
        expected_counts, _ = np.histogram(expected, bins=breakpoints)
        actual_counts, _ = np.histogram(actual, bins=breakpoints)
        expected_pct = expected_counts / len(expected)
        actual_pct = actual_counts / len(actual)
        expected_pct = np.where(expected_pct == 0, 0.0001, expected_pct)
        actual_pct = np.where(actual_pct == 0, 0.0001, actual_pct)
        psi = np.sum(
            (actual_pct - expected_pct)
            * np.log(actual_pct / expected_pct)
        )

        return psi, breakpoints, expected_pct, actual_pct

    def drift_status(self, psi):

        if psi < 0.1:
            return "No Drift"

        elif psi < 0.25:
            return "Moderate Drift"

        else:
            return "Significant Drift"

    def plot_distribution(self, expected, actual, column):

        plt.figure(figsize=(8, 5))

        plt.hist(expected, bins=10, alpha=0.5, label="Baseline")

        plt.hist(actual, bins=10, alpha=0.5, label="Current")

        plt.title(f"{column} Distribution Comparison")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.legend()

        plt.show()

    def plot_psi_bins(self, expected_pct, actual_pct, column):

        x = np.arange(len(expected_pct))
        width = 0.4

        plt.figure(figsize=(8, 5))

        plt.bar(x - width/2, expected_pct, width, label="Baseline")

        plt.bar(x + width/2, actual_pct, width, label="Current")

        plt.title(f"{column} PSI Bin Comparison")
        plt.xlabel("Bin Number")
        plt.ylabel("Proportion")
        plt.legend()

        plt.show()

    def generate_report(self):

        numeric_columns = ["Temperature_C", "Humidity_pct",
                           "Precipitation_mm", "Wind_Speed_kmh"]

        print("Data Drift Report")

        for col in numeric_columns:
            psi, breakpoints, expected_pct, actual_pct = self.calculate_psi(
                self.baseline_df[col],
                self.current_df[col])
            print(f"Feature: {col}")
            print(f"PSI : {psi}")
            print(f"Status : {self.drift_status(psi)}")

            self.plot_distribution(self.baseline_df[col],
                                   self.current_df[col], col)
            self.plot_psi_bins(expected_pct, actual_pct, col)


org_df_path = Path("Task_2\\data\\weather_data.csv")
drifted_df_path = Path("Task_2\\data\\weather_drifted_data.csv")
drift = DataDrift(org_df_path, drifted_df_path)
drift.generate_report()

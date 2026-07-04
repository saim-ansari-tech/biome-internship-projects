import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class EDA:

    def __init__(self, df):
        self.df = df

    def clean_placeholder(self):
        self.df.replace("?", np.nan, inplace=True)

    def dataset_summary(self):
        summary = {
            "Rows": self.df.shape[0],
            "Columns": self.df.shape[1],
            "Duplicate Rows": self.df.duplicated().sum(),
            "Total Missing Values": int(self.df.isnull().sum().sum()),
            "Missing Percentage": round(
                (self.df.isnull().sum() / self.df.size) * 100, 2
            ),
        }
        return summary

    def feature_summary(self, feature):
        summary = {
            "Feature": feature,
            "Data Type": str(self.df[feature].dtype),
            "Total Values": len(self.df),
            "Unique Values": self.df[feature].nunique(dropna=True),
            "Missing Count": self.df[feature].isnull().sum(),
            "Missing Percentage": round(
                (self.df[feature].isnull().sum() / len(self.df)) * 100, 2
            ),
            "Question Mark Count": (self.df[feature] == "?").sum(),
            "Most Frequent Value": (
                self.df[feature].mode().iloc[0]
                if not self.df[feature].mode().empty
                else np.nan
            ),
            "Most Frequent Count": self.df[feature].value_counts(
                dropna=False).iloc[0],
        }
        return summary

    def missing_value_report(self):

        report = pd.DataFrame(
            {
                "Feature": self.df.columns,
                "Missing Count": self.df.isnull().sum().values,
                "Missing Percentage": (self.df.isnull().sum() /
                                       len(self.df) * 100)
                .round(2)
                .values,
            }
        )
        report = report.sort_values(
            by="Missing Percentage", ascending=False
        ).reset_index(drop=True)

        return report

    def question_mark_report(self):

        report = pd.DataFrame(
            {
                "Feature": self.df.columns,
                "Quetion Mark Count": (self.df == "?").sum().values,
                "Question Mark Percentage": (
                    (self.df == "?").sum() / len(self.df) * 100
                )
                .round(2)
                .values,
            }
        )

        report = report[report["Question Mark Count"] > 0]
        report = report.sort_values(
            by="Question Mark Count",
            ascending=False,
        ).reset_index(drop=True)

        return report

    def duplicated_report(self):

        report = {
            "Total Rows": len(self.df),
            "Duplicate Rows": self.df.duplicated().sum(),
            "Duplicate Percentage": round(
                (self.df.duplicated().sum() / len(self.df)) * 100, 2
            ),
        }
        return report

    def value_distribution(self, feature):
        counts = self.df[feature].value_counts(dropna=False)
        percentages = (
            self.df[feature].value_counts(dropna=False, normalize=True) * 100
        ).round(2)

        report = pd.DataFrame(
            {
                "Value": counts.index,
                "Count": counts.values,
                "Percentage": percentages.values,
            }
        )

        return report

    def numerical_summary(self, feature):
        summary = {
            "Feature": feature,
            "Mean": self.df[feature].mean(),
            "Median": self.df[feature].median(),
            "Mode": self.df[feature].mode().iloc[0],
            "Minimum": self.df[feature].min(),
            "Maximum": self.df[feature].max(),
            "Standard Deviation": self.df[feature].std(),
            "Variance": self.df[feature].var(),
            "Skewness": self.df[feature].skew(),
            "Kurtosis": self.df[feature].kurt(),
            "Q1": self.df[feature].quantile(0.25),
            "Q2": self.df[feature].quantile(0.50),
            "Q3": self.df[feature].quantile(0.75),
        }

        return summary

    def categorical_summary(self, feature):
        summary = {
            "Feature": feature,
            "dtype": self.df[feature].dtype(),
            "No of Cat": self.df[feature].nunique(),
            "Missing count": self.df[feature].isnull().sum(),
            "Missing Percentage": round(self.df[feature].
                                        isnull().mean() * 100,
                                        2),
            "Mode": self.df[feature].mode(dropna=True),
            "Mode freq": self.df[feature].value_counts(dropna=False).iloc[0],
        }
        return summary

    def outlier_report(self, feature):

        q1 = self.df[feature].quantile(0.25)
        q3 = self.df[feature].quantile(0.75)
        iqr = q3 - q1
        low = q1 - 1.5 * iqr
        upper = q1 + 1.5 * iqr
        outliers = self.df[(self.df[feature] < low) |
                           (self.df[feature] > upper)]

        summary = {
            "Q1": q1,
            "Q3": q3,
            "IQR": iqr,
            "Lower Bound": low,
            "Upper Bound": upper,
            "Outlier Count": len(outliers),
            "Outlier Percentage": round(len(outliers) / len(self.df) * 100, 2),
        }
        return summary

    def correlation_matrix(self):
        numeric_df = self.df.select_dtypes(include="number")
        corr = numeric_df.corr()

        return corr

    def plot_histogram(self, feature):
        plt.Figure(figsize=(5, 5))
        sns.histplot(data=self.df, x=feature, kde=True)
        plt.show()

    def plot_boxplot(self, feature):
        plt.Figure(figsize=(5, 5))
        sns.boxplot(data=self.df, x=feature)
        plt.show()

    def plot_countplot(self, feature):
        plt.Figure(figsize=(5, 5))
        sns.countplot(data=self.df, x=feature)
        plt.show()

    def plot_missing_values(self):
        missing_percentage = (self.df.isnull().sum() / len(self.df)) * 100
        missing_percentage = missing_percentage[missing_percentage > 0]
        missing_percentage = missing_percentage.sort_values(ascending=False)

        if missing_percentage.empty:
            print("No missing values found in the dataset.")
            return None

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=missing_percentage.index,
                    y=missing_percentage.values, ax=ax)

        ax.set_title("Missing Value Percentage by Feature")
        ax.set_xlabel("Features")
        ax.set_ylabel("Missing Percentage (%)")

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        return fig

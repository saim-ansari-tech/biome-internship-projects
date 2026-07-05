import pandas as pd
import numpy as np


class Preprocessing:
    def __init__(self, df):
        self.df = df

    def drop_cols(self, cols):
        self.df.drop(columns=cols, inplace=True)

    def drop_category_rows(self, column, category):
        self.df = self.df[
            self.df[column] != category
        ]

    def drop_rows_by_values(self, column, values):
        self.df = self.df[
            ~self.df[column].isin(values)
        ]

    def clean_placeholder(self):
        self.df.replace("?", np.nan, inplace=True)

        def question_mark_report(self):
            self.report = pd.DataFrame(
                {
                    "Feature": self.df.columns,
                    "Question Mark Count": (self.df == "?").sum().values,
                    "Question Mark Percentage": (
                        (self.df == "?").sum() / len(self.df) * 100
                    )
                    .round(2)
                    .values,
                }
            )

    def convert_dtype_category(self, cols):

        for col in cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype("category")

    def convert_dtype_numeric(self, cols):

        for col in cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col])

    def handle_categorical_missing_vals(self, cols, value):

        for col in cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna(value)

    def handle_numeric_missing_vals(self, cols, strategy):

        for col in cols:
            if col in self.df.columns:
                if strategy == "mean":
                    self.df[cols] = self.df[col].mean()

                elif strategy == "median":
                    self.df[cols] = self.df[col].median()

                elif strategy == "mode":
                    self.df[cols] = self.df[col].mode()[0]

    def handle_rare_categories(self, cols, min_count):

        for col in cols:
            if col in self.df.columns:
                counts = self.df[col].value_counts()
                rare_category = counts[counts < min_count].index
                self.df[col] = self.df[col].replace(rare_category, "other")

    def transform_target(self):
        self.df["readmitted"] = self.df["readmitted"].map({
            "<30": 1,
            ">30": 0,
            "NO": 0,
        })

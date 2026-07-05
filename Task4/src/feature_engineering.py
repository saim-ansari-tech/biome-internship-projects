import pandas as pd


class FeatureEngineering:

    def __init__(self, df):
        self.df = df

    def transform_age(self):
        age_mapping = {
            "[0-10)": 0,
            "[10-20)": 1,
            "[20-30)": 2,
            "[30-40)": 3,
            "[40-50)": 4,
            "[50-60)": 5,
            "[60-70)": 6,
            "[70-80)": 7,
            "[80-90)": 8,
            "[90-100)": 9,
        }

        self.df["age"] = self.df["age"].map(age_mapping)

    def total_visits(self):
        self.df["total_visits"] = (
            self.df["number_outpatient"]
            + self.df["number_emergency"]
            + self.df["number_inpatient"]
        )

    def long_stay(self):
        self.long_stay_threshold = self.df["time_in_hospital"].quantile(0.75)
        self.df["long_stay"] = (
            self.df["time_in_hospital"] > self.long_stay_threshold
        ).astype(int)

    def high_medications(self):
        self.high_medications_threshold = self.df[
            "num_medications"].quantile(0.75)
        self.df["high_medications"] = (
            self.df["num_medications"] > self.high_medications_threshold
        ).astype(int)

    def multiple_diagnoses(self):
        self.multiple_diagnoses_threshold = self.df[
            "number_diagnoses"].quantile(0.75)
        self.df["multiple_diagnoses"] = (
            self.df["number_diagnoses"] > self.multiple_diagnoses_threshold
        ).astype(int)

    def categorize_diagnosis(self, code):
        if pd.isna(code):
            return "Unknown"

        code = str(code)

        if code.startswith("V"):
            return "Supplementary"

        if code.startswith("E"):
            return "Injury"

        try:
            code = float(code)
        except ValueError:
            return "Other"

        if 390 <= code <= 459 or code == 785:
            return "Circulatory"

        elif 460 <= code <= 519 or code == 786:
            return "Respiratory"

        elif 520 <= code <= 579 or code == 787:
            return "Digestive"

        elif 250 <= code < 251:
            return "Diabetes"

        elif 800 <= code <= 999:
            return "Injury"

        elif 710 <= code <= 739:
            return "Musculoskeletal"

        elif 580 <= code <= 629 or code == 788:
            return "Genitourinary"

        elif 140 <= code <= 239:
            return "Neoplasms"

        else:
            return "Other"

    def engineer_diagnosis_groups(self):
        diagnosis_cols = ["diag_1", "diag_2", "diag_3"]

        for col in diagnosis_cols:
            self.df[f"{col}_group"] = (
                self.df[col]
                .apply(self.categorize_diagnosis)
            )
    
    def drop_original_diagnosis_cols(self):
        self.df.drop(
            columns=["diag_1", "diag_2", "diag_3"],
            inplace=True,
        )

import re
import pandas as pd
import string
import os

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class DataPreprocessing:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()

    def get_df(self):
        return self.df

    def remove_duplicates(self):
        before = len(self.df)

        self.df.drop_duplicates(inplace=True)
        self.df.reset_index(drop=True, inplace=True)

        after = len(self.df)

        print("Duplicate Removal")
        print(f"Rows Before : {before}")
        print(f"Rows After  : {after}")
        print(f"Removed     : {before - after}")

    def convert_timestamp(self):
        self.df["timestamp"] = pd.to_datetime(self.df
                                              ["timestamp"],
                                              errors="coerce")
        invalid = self.df["timestamp"].isna().sum()

        print("Timestamp converted successfully")
        print(f"Invalid Timestamp {invalid}")

    def combine_text(self):
        self.df["combined_text"] = (
            self.df["post_text"].fillna("") + " " +
            self.df["hashtags"].fillna("")
        )

        print("Text Column created successfully")

    def preprocess_text(self, text: str):

        if pd.isna(text):
            return ""

        text = str(text).lower()

        text = re.sub(r"https?://\S+|www\.\S+", "", text)

        text = re.sub(r"@\w+", "", text)

        text = text.replace(";", " ").replace("#", "")

        text = text.translate(str.maketrans("", "", string.punctuation))

        text = re.sub(r"\d+", "", text)

        words = text.split()
        if not words:
            return ""

        words = [
            self.lemmatizer.lemmatize(word)
            for word in words
            if word not in self.stop_words
        ]

        return " ".join(words).strip()

    def clean_text(self):
        self.df["cleaned_text"] = (
            self.df["combined_text"]
            .apply(self.preprocess_text)
        )

        print("Text Preprocessing completed successfully")

    def preprocess(self):
        print("Starting Data Preprocessing...")

        self.remove_duplicates()
        self.convert_timestamp()
        self.combine_text()
        self.clean_text()

        print("Preprocessing Completed Successfully!")

        return self.df

    def save_preprocessed_data(self, output_path: str):

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        self.df.to_csv(output_path, index=False)

        print(f"Processed dataset saved to:\n{output_path}")

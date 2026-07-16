import re
import pandas as pd
import os
from ftfy import fix_text
import emoji
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


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

        if not isinstance(text, str):
            return ""

        text = fix_text(str(text))

        text = text.lower()

        text = re.sub(r"https?://\S+|www\.\S+", " ", text)

        text = re.sub(r"\b(http|https|www)\b", " ", text)

        text = re.sub(r"@\w+", " ", text)

        text = re.sub(r"#(\w+)", r"\1", text)

        text = emoji.replace_emoji(text, replace="")

        text = (
            text.replace("—", " ")
            .replace("–", " ")
            .replace("…", " ")
            .replace("“", " ")
            .replace("”", " ")
            .replace("‘", " ")
            .replace("’", " ")
        )

        text = re.sub(r"[^\w\s]", " ", text)

        text = re.sub(r"\d+", " ", text)

        text = re.sub(r"\s+", " ", text).strip()

        tokens = word_tokenize(text)

        tokens = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if (
                token not in self.stop_words
                and len(token) > 2
                and token.isascii()
                and token not in {
                    "source",
                    "article",
                    "link",
                    "http",
                    "https",
                    "www",
                }
            )
        ]

        return " ".join(tokens)

    def clean_text(self):
        self.df["cleaned_text"] = (
            self.df["combined_text"]
            .apply(self.preprocess_text)
        )

        print("Text Preprocessing completed successfully")

    def detect_language(self, text):
        try:
            return detect(str(text))

        except LangDetectException:
            return "unknown"

    def keep_english_posts(self):

        before = len(self.df)

        self.df["language"] = (
            self.df["combined_text"]
            .apply(self.detect_language)
        )

        self.df = (
            self.df[self.df["language"] == "en"]
            .copy()
        )

        after = len(self.df)

        print("=" * 60)
        print("English Language Filtering")
        print("=" * 60)
        print(f"Rows Before : {before}")
        print(f"Rows After  : {after}")
        print(f"Removed     : {before - after}")

    def preprocess(self):
        print("Starting Data Preprocessing...")

        self.remove_duplicates()
        self.convert_timestamp()
        self.combine_text()
        self.keep_english_posts()
        self.clean_text()

        print("Preprocessing Completed Successfully!")

        return self.df

    def save_preprocessed_data(self, output_path: str):

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        self.df.to_csv(output_path, index=False)

        print(f"Processed dataset saved to:\n{output_path}")

    def load_preprocessed_data(
        self,
        input_path: str,
    ):

        self.df = pd.read_csv(
            input_path,
            parse_dates=["timestamp"],
        )

        print(
            f"Processed dataset loaded successfully:\n"
            f"{input_path}"
        )

        return self.df

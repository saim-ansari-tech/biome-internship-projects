import joblib
import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    confusion_matrix
)


class ModelTrainer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.vectorizer = None
        self.model = None
        self.models = {}
        self.results = []
        self.best_model = None
        self.best_model_name = None
        self.best_accuracy = 0

        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.X_train_tfidf = None
        self.X_test_tfidf = None

    def split_data(self, test_size: float = 0.2, random_state: int = 42):
        X = self.df["cleaned_text"]
        y = self.df["topic"]

        (
            self.X_train,
            self.X_test,
            self.y_train,
            self.y_test
        ) = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )

        print("Dataset Split Completed")
        print(f"Training Samples : {len(self.X_train)}")
        print(f"Testing Samples  : {len(self.X_test)}")

    def vectorize_text(self,
                       max_features: int = 10000,
                       ngram_range: tuple = (1, 2)):

        self.vectorizer = TfidfVectorizer(
            max_features=max_features, ngram_range=ngram_range
        )
        self.X_train_tfidf = self.vectorizer.fit_transform(self.X_train)
        self.X_test_tfidf = self.vectorizer.transform(self.X_test)

        print("TF-IDF Vectorization Completed")
        print(f"Vocabulary Size : {len(self.vectorizer.vocabulary_)}")
        print(f"Training Shape  : {self.X_train_tfidf.shape}")
        print(f"Testing Shape   : {self.X_test_tfidf.shape}")

    def train_models(self):

        self.models = {
            "Logistic Regression": LogisticRegression(
                max_iter=1000,
                random_state=42),
            "Linear SVM": LinearSVC(random_state=42),
            "Multinomial Naive Bayes": MultinomialNB(),
            "Random Forest": RandomForestClassifier(
                n_estimators=200,
                random_state=42),
        }

        print("Training Multiple Models")

        for name, model in self.models.items():

            print(f"\nTraining {name}...")

            model.fit(self.X_train_tfidf, self.y_train)

            predictions = model.predict(self.X_test_tfidf)

            accuracy = accuracy_score(self.y_test, predictions)

            self.results.append({"Model": name, "Accuracy": accuracy})

            print(f"Accuracy : {accuracy:.4f}")

            if accuracy > self.best_accuracy:
                self.best_accuracy = accuracy
                self.best_model = model
                self.best_model_name = name

        print("Best Model")
        print(f"Model    : {self.best_model_name}")
        print(f"Accuracy : {self.best_accuracy:.4f}")

    def evaluate_model(self):

        predictions = self.best_model.predict(self.X_test_tfidf)

        accuracy = accuracy_score(self.y_test, predictions)

        print("Model Evaluation")

        print(f"Accuracy : {accuracy:.4f}")

        print("\nClassification Report\n")

        print(classification_report(self.y_test, predictions))

        print("\nConfusion Matrix\n")

        print(confusion_matrix(self.y_test, predictions))

    def save_model(self, model_dir: str = "models"):
        os.makedirs(model_dir, exist_ok=True)

        joblib.dump(
            self.best_model,
            os.path.join(
                model_dir,
                "topic_classifier.pkl"
            )
        )

        joblib.dump(
            self.vectorizer,
            os.path.join(
                model_dir,
                "tfidf_vectorizer.pkl"
            )
        )

        print("Model Saved Successfully")
        print(f"Directory : {model_dir}")

    def train_pipeline(self):

        print("Starting Model Training...")

        self.split_data()
        self.vectorize_text()
        self.train_models()
        self.evaluate_model()
        self.save_model()

        print("Training Pipeline Completed")

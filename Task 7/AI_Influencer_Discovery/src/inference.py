import joblib
import pandas as pd


class TopicPredictor:

    def __init__(
        self,
        model_path: str = "models/topic_classifier.pkl",
        vectorizer_path: str = "models/tfidf_vectorizer.pkl",
    ):

        self.model_path = model_path
        self.vectorizer_path = vectorizer_path

        self.model = None
        self.vectorizer = None

    def load_model(self):

        self.model = joblib.load(self.model_path)
        self.vectorizer = joblib.load(self.vectorizer_path)

        print("Model Loaded Successfully")

    def predict(self, text: str):

        text_vector = self.vectorizer.transform([text])

        prediction = self.model.predict(text_vector)[0]

        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba(text_vector)[0]

            print("=" * 60)
            print("Prediction Probabilities")
            print("=" * 60)

            for label, prob in zip(self.model.classes_, probabilities):
                print(f"{label:<12}: {prob:.4f}")

        return prediction

    def predict_batch(self, texts: pd.Series):

        text_vectors = self.vectorizer.transform(texts)

        predictions = self.model.predict(text_vectors)

        return predictions

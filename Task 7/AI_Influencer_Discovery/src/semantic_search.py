from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import os


class SemanticSearch:
    def __init__(self):
        self.model = None
        self.embeddings = None
        self.df = None

    def load_model(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Model loaded successfully")

    def generate_embeddings(self, df: pd.DataFrame,
                            text_column="cleaned_text"):
        self.df = df.copy()

        print("Generate Post Embeddings....")

        self.embeddings = self.model.encode(
            self.df[text_column].tolist(),
            show_progress_bar=True,
            convert_to_numpy=True
        )
        print("Embedding generated successfully")

    def save_embeddings(self, output_path: str):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        np.save(output_path, self.embeddings)

        print("Embedding save successfully")

    def load_embeddings(self, input_path: str, df: pd.DataFrame):
        self.embeddings = np.load(input_path)
        self.df = df.copy()

        print("Embedding loaded Successfully")

    def search_posts(self, query: str, top_k: int = 100):
        query_embedding = self.model.encode(
            [query], show_progress_bar=True, convert_to_numpy=True
        )

        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        results = self.df.copy()
        results["semantic_score"] = similarities
        results = (
            results.sort_values(by="semantic_score", ascending=False)
            .head(top_k)
            .reset_index(drop=True)
        )

        return results

    def recommend_influencers(
        self,
        query: str,
        ranked_df: pd.DataFrame,
        top_posts: int = 10,
        top_influencers: int = 10,
    ):

        similar_posts = self.search_posts(query=query, top_k=top_posts)

        similar_posts["post_preview"] = (
            similar_posts["post_text"]
            .str[:250] + "..."
        )

        recommendations = ranked_df[
            ranked_df["user_name"].isin(similar_posts["user_name"])
        ].copy()

        recommendations = (
            recommendations.drop_duplicates(subset="user_name")
            .sort_values(by="influencer_score", ascending=False)
            .head(top_influencers)
            .reset_index(drop=True)
        )

        return similar_posts, recommendations

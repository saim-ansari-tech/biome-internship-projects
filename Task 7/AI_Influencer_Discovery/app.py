from flask import (
    Flask,
    render_template,
    request,
)

import pandas as pd

from src.preprocessing import DataPreprocessing
from src.ranking import InfluencerRanking
from src.inference import TopicPredictor
from src.semantic_search import SemanticSearch


app = Flask(__name__)


preprocessing = DataPreprocessing(pd.DataFrame())

processed_df = preprocessing.load_preprocessed_data(
    r"D:\Internship_projects\biome-internship-projects"
    r"\Task 7\AI_Influencer_Discovery"
    r"\artifacts\processed_data.csv"
)

print("proc_df_col", processed_df.columns)

print("topics", processed_df["topic"].unique())

print("len", len(processed_df))

ranking = InfluencerRanking(processed_df)

ranking.load_rankings(
    r"D:\Internship_projects\biome-internship-projects"
    r"\Task 7\AI_Influencer_Discovery"
    r"\artifacts\ranked_influencers.csv"
)

predictor = TopicPredictor()
predictor.load_model()

semantic = SemanticSearch()
semantic.load_model()

semantic.load_embeddings(
    r"D:\Internship_projects\biome-internship-projects"
    r"\Task 7\AI_Influencer_Discovery"
    r"\artifacts\post_embeddings.npy",
    processed_df,
)


@app.route("/")
def home():

    return render_template("index.html")


@app.route(
    "/topic",
    methods=["GET", "POST"]
)
def topic():
    topics = sorted(
        processed_df["topic"].unique()
    )

    results = None

    if request.method == "POST":

        selected_topic = request.form["topic"]

        results = ranking.get_top_influencers(
            selected_topic
        )

        results = results.to_dict(
            orient="records"
        )

    return render_template(
        "topic.html",
        topics=topics,
        results=results,
    )


@app.route(
    "/recommend",
    methods=["GET", "POST"]
)
def recommend():

    predicted_topic = None
    results = None

    if request.method == "POST":

        text = request.form["query"]

        predicted_topic = predictor.predict(
            text
        )

        results = ranking.get_top_influencers(
            predicted_topic
        )

        results = results.to_dict(
            orient="records"
        )

    return render_template(
        "recommend.html",
        predicted_topic=predicted_topic,
        results=results,
    )


@app.route(
    "/semantic",
    methods=["GET", "POST"]
)
def semantic_search():

    similar_posts = None
    recommendations = None

    if request.method == "POST":

        query = request.form["query"]

        similar_posts, recommendations = (
            semantic.recommend_influencers(
                query=query,
                ranked_df=ranking.ranked_df,
            )
        )

        similar_posts = (
            similar_posts.to_dict(
                orient="records"
            )
        )

        recommendations = (
            recommendations.to_dict(
                orient="records"
            )
        )

    return render_template(
        "semantic.html",
        similar_posts=similar_posts,
        recommendations=recommendations,
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )

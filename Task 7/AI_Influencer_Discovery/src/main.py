from preprocessing import DataPreprocessing
from ranking import InfluencerRanking
from inference import TopicPredictor
from semantic_search import SemanticSearch
import pandas as pd


def main():

    print("AI Influencer Discovery System")

    preprocessing = DataPreprocessing(pd.DataFrame())
    processed_df = (
        preprocessing.load_preprocessed_data(
            r"D:\Internship_projects\biome-internship-projects"
            r"\Task 7\AI_Influencer_Discovery"
            r"\artifacts\processed_data.csv"
        )
    )

    ranking = InfluencerRanking(processed_df)
    ranking.load_rankings(
        r"D:\Internship_projects\biome-internship-projects"
        r"\Task 7\AI_Influencer_Discovery"
        r"\artifacts\ranked_influencers.csv"
    )

    semantic = SemanticSearch()
    semantic.load_model()
    semantic.load_embeddings(
        r"D:\Internship_projects\biome-internship-projects"
        r"\Task 7\AI_Influencer_Discovery"
        r"\artifacts\post_embeddings.npy",
        processed_df,
    )

    predictor = TopicPredictor()
    predictor.load_model()


if __name__ == "__main__":
    main()

from preprocessing import DataPreprocessing
from trainer import ModelTrainer
from ranking import InfluencerRanking
from semantic_search import SemanticSearch

import pandas as pd


def main():

    print("Training AI Influencer Discovery System")

    df = pd.read_csv(
        r"D:\Internship_projects\biome-internship-projects"
        r"\Task 7\AI_Influencer_Discovery\data"
        r"\scraped_posts (2).csv"
    )

    preprocessing = DataPreprocessing(df)

    processed_df = preprocessing.preprocess()

    preprocessing.save_preprocessed_data(
        r"D:\Internship_projects\biome-internship-projects"
        r"\Task 7\AI_Influencer_Discovery"
        r"\artifacts\processed_data.csv"
    )

    trainer = ModelTrainer(processed_df)
    trainer.train_pipeline()

    ranking = InfluencerRanking(processed_df)

    ranking.ranking_pipeline()

    ranking.save_rankings(
        r"D:\Internship_projects\biome-internship-projects"
        r"\Task 7\AI_Influencer_Discovery"
        r"\artifacts\ranked_influencers.csv"
    )

    semantic = SemanticSearch()

    semantic.load_model()

    semantic.generate_embeddings(processed_df)

    semantic.save_embeddings(
        r"D:\Internship_projects\biome-internship-projects"
        r"\Task 7\AI_Influencer_Discovery"
        r"\artifacts\post_embeddings.npy"
    )

    print("\nTraining completed successfully!")


if __name__ == "__main__":
    main()

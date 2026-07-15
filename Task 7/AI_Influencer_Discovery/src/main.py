from preprocessing import DataPreprocessing
from trainer import ModelTrainer
from ranking import InfluencerRanking
from inference import TopicPredictor

import pandas as pd


def main():

    print("AI Influencer Discovery System")

    df = pd.read_csv(
        r"D:\Internship_projects\biome-internship-projects\
            Task 7\AI_Influencer_Discovery\data\scraped_posts (2).csv"
    )

    preprocessing = DataPreprocessing(df)
    processed_df = preprocessing.preprocess()

    trainer = ModelTrainer(processed_df)
    trainer.train_pipeline()

    ranking = InfluencerRanking(processed_df)
    ranking.ranking_pipeline()

    predictor = TopicPredictor()
    predictor.load_model()

    while True:

        print("AI Influencer Discovery System")
        print("1. Search by Topic")
        print("2. AI Recommendation")
        print("3. Exit")

        choice = input("\nSelect Option: ").strip()

        if choice == "1":
            print("\nAvailable Topics")

            for topic in sorted(processed_df["topic"].unique()):
                print(topic)
            topic = input("\nEnter a topic: ").strip()

            ranking.get_top_influencers(topic)

        elif choice == "2":

            text = input(
                "\nDescribe what content you are interested in:\n\n"
                ).strip()

            if not text:
                print("Please enter some text.")
                continue

            predicted_topic = predictor.predict(text)

            print("\nPredicted Topic:", predicted_topic)

            print("\nTop Influencers\n")

            ranking.get_top_influencers(predicted_topic)

        elif choice == "3":

            print("\nThank you for using AI Influencer Discovery System!")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()

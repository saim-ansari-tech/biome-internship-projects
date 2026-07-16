import pandas as pd
import numpy as np
import os


class InfluencerRanking:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.ranked_df = None

    def get_df(self):
        return self.ranked_df

    def calculate_engagement_score(self):
        self.df["engagement_score"] = (
            0.5 * self.df["likes"] + 0.3 * self.df
            ["comments"] + 0.2 *
            self.df["shares"]
        )

        self.df.loc[self.df["verified"], "engagement_score"] *= 1.10

        print("Engagement Score Calculated")

    def aggregate_users(self):

        self.ranked_df = self.df.groupby([
            "user_name",
            "topic"],
            as_index=False
        ).agg(
            followers=("followers", "max"),
            following=("following", "max"),
            verified=("verified", "max"),
            post_count=("post_text", "count"),
            avg_likes=("likes", "mean"),
            avg_comments=("comments", "mean"),
            avg_shares=("shares", "mean"),
            avg_engagement=("engagement_score", "mean"),
        )

        print("User Aggregation Completed")
        print(f"Total Influencers : {len(self.ranked_df)}")

    def calculate_influencer_score(self):

        self.ranked_df["influencer_score"] = (
            self.ranked_df["avg_engagement"] * 0.50
            + self.ranked_df["avg_comments"] * 0.20
            + self.ranked_df["avg_shares"] * 0.15
            + np.log1p(self.ranked_df["followers"]) * 0.15
        )

        self.ranked_df.loc[self.ranked_df["verified"],
                           "influencer_score"] *= 1.10

        print("Influencer Score Calculated")

    def rank_influencers(self):

        self.ranked_df = self.ranked_df.sort_values(
            by="influencer_score", ascending=False
        ).reset_index(drop=True)

        print("Influencers Ranked Successfully")

    def get_top_influencers(self, topic: str, top_k: int = 10):

        result = self.ranked_df[
            self.ranked_df["topic"].str.lower() == topic.lower()
        ].head(top_k)

        if result.empty:
            print(f"\nNo influencers found for topic: {topic}")
        else:
            print(result)

        return result

    def ranking_pipeline(self):

        print("Starting Influencer Ranking...")

        self.calculate_engagement_score()
        self.aggregate_users()
        self.calculate_influencer_score()
        self.rank_influencers()

        print("Ranking Pipeline Completed")

        return self.ranked_df

    def save_rankings(
        self,
        output_path: str,
    ):

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True,
        )

        self.ranked_df.to_csv(
            output_path,
            index=False,
        )

        print(
            f"Rankings saved successfully:\n"
            f"{output_path}"
        )

    def load_rankings(
        self,
        input_path: str,
    ):

        self.ranked_df = pd.read_csv(
            input_path
        )

        print(
            f"Rankings loaded successfully:\n"
            f"{input_path}"
        )

        return self.ranked_df

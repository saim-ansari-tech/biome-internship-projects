import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def analyze_metadata():
    df = pd.read_csv("biome-internship-projects\\Task5\\data\\metadata.csv")
    print("--------------------Report------------------------------")
    print(f"Shape: {df.shape}")
    print(f"{df.head()}")
    print(f"{df.info()}")
    print(f"{df.describe()}")
    print(f"Unique Sample Rate: {df['sample_rate'].nunique()}")
    print(f"Unique Channels : {df['channels'].nunique()}")
    print(f"Unique Format: {df['format'].nunique()}")
    print(f"Unique Subtype: {df['subtype'].nunique()}")
    print(f"No. of Unique Speakers : {df['speaker_id'].nunique()}")
    print(f"No. of Unique Videos : {df['video_id'].nunique()}")
    speaker_recordings = df["speaker_id"].value_counts()
    print(f"No. of Recordings: {speaker_recordings}")
    print(f"Maximum recordings per speaker : {speaker_recordings.max()}")
    print(f"Minimum recordings per speaker : {speaker_recordings.min()}")
    print(f"Average recordings per speaker : {speaker_recordings.mean():.2f}")
    print(f"Median recordings per speaker : {speaker_recordings.median()}")
    print(f"Missing Values: {df.isnull().sum()}")
    print(f"Duplicates values : {df.duplicated().sum()}")

    return df


def plot_histogram(df):
    plt.figure(figsize=(5, 5))
    sns.histplot(data=df, x="duration", kde=True)
    plt.title("Duration Histogram")
    plt.show()

    no_recording = df["speaker_id"].value_counts()
    plt.figure(figsize=(5, 5))
    sns.histplot(data=df, x=no_recording, kde=True)
    plt.title("Distribution of Recordings per Speaker")
    plt.show()


def main():
    df = analyze_metadata()
    plot_histogram(df)


if __name__ == "__main__":
    main()

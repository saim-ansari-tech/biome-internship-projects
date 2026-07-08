import pandas as pd

class DatasetPreparation:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)

    def encode_labels(self):
        self.df['label'] = (self.df['speaker_id'].astype('category').cat.codes)
        return self.df
    

def main():
    dataset = DatasetPreparation(r"D:\Internship_projects\biome-internship-projects\Task5\data\metadata.csv")

    df = dataset.encode_labels()

    df.to_csv("metadata_encoded.csv", index=False)

    print("Metadata encoded successfully!")


if __name__ == "__main__":
    main()

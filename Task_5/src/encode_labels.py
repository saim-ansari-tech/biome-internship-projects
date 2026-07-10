import pandas as pd

df = pd.read_csv(
    r"D:\Internship_projects\biome-internship-projects\
        Task_5\data\metadata_subset.csv"
)
unique_labels = sorted(df["label"].unique())

label_map = {label: idx for idx, label in enumerate(unique_labels)}

df["label"] = df["label"].map(label_map)
df.to_csv(
    r"D:\Internship_projects\biome-internship-projects\
        Task_5\data\metadata_subset.csv",
    index=False,
)

print("Labels encoded successfully!")
print(label_map)

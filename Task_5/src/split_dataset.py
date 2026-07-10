import pandas as pd

from sklearn.model_selection import train_test_split

metadata = pd.read_csv(
    r"biome-internship-projects\
        Task_5\data\metadata_subset.csv"
)

train_df, temp_df = train_test_split(

    metadata,

    test_size=0.30,

    stratify=metadata["label"],

    random_state=42

)

val_df, test_df = train_test_split(

    temp_df,

    test_size=0.50,

    stratify=temp_df["label"],

    random_state=42

)

train_df.to_csv(
    "train.csv",
    index=False
)

val_df.to_csv(
    "val.csv",
    index=False
)

test_df.to_csv(
    "test.csv",
    index=False
)


print("Train:", len(train_df))
print("Validation:", len(val_df))
print("Test:", len(test_df))

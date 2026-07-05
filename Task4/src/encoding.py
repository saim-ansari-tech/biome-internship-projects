from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
import pandas as pd


class Encoding:

    def __init__(self, df):
        self.df = df

    def one_hot_encode(self, cols):
        encoder = OneHotEncoder(sparse=False)
        encoded = encoder.fit_transform(self.df[cols])

        encoded_df = pd.DataFrame(
            encoded,
            columns=encoder.get_feature_names_out(cols),
            index=self.df.index
        )

        self.df = self.df.drop(columns=cols)
        self.df = pd.concat([self.df, encoded_df], axis=1)

    def binary_encode(self, col, mapping):
        self.df[col] = self.df[col].map(mapping)

    def ordinal_encode(self, cols, categories):
        encoder = OrdinalEncoder(categories=categories)
        self.df[cols] = encoder.fit_transform(
            self.df[cols])

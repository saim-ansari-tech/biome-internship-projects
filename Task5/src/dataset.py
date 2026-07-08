import pandas as pd
import torch
from torch.utils.data import Dataset
from preprocessing import Preprocessing
from feature_extraction import FeatureExtraction


class SpeakerDataset(Dataset):
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        row = self.df.iloc[index]

        audio_path = row["file_path"]
        label = row["label"]

        preproc = Preprocessing(audio_path)
        preproc.load_audio_file()
        preproc.random_crop(3)

        feature = FeatureExtraction(preproc.y, preproc.sr)
        feature.generate_magnitude_spectrogram()
        feature.normalize_features()

        feature_tensor = torch.tensor(feature.magnitude, dtype=torch.float32)
        feature_tensor = feature_tensor.unsqueeze(0)
        label_tensor = torch.tensor(label, dtype=torch.long)

        return feature_tensor, label_tensor

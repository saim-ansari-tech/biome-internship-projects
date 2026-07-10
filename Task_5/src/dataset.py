import pandas as pd
import torch
import torchaudio
import torchaudio.transforms as T
import soundfile as sf
from torch.utils.data import Dataset

import config


class SpeakerDataset(Dataset):
    def __init__(self, csv_path):
        self.metadata = pd.read_csv(csv_path)

        self.mel_transform = T.MelSpectrogram(
            sample_rate=config.SAMPLE_RATE,
            n_fft=config.N_FFT,
            win_length=config.WIN_LENGTH,
            hop_length=config.HOP_LENGTH,
            n_mels=config.N_MELS,
            power=2.0,
        )
        self.crop_samples = 3 * 16000

    def __len__(self):
        return len(self.metadata)

    def __getitem__(self, index):
        row = self.metadata.iloc[index]

        file_path = row["file_path"]
        label = row["label"]

        try:
            waveform, sample_rate = torchaudio.load(file_path)

        except Exception:

            data, sample_rate = sf.read(file_path)

            waveform = torch.from_numpy(data).float()

            if waveform.ndim == 1:
                waveform = waveform.unsqueeze(0)
            else:
                waveform = waveform.T

        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)

        length = waveform.shape[1]

        if length > self.crop_samples:

            start = torch.randint(0, length - self.crop_samples + 1,
                                  (1,)).item()

            waveform = waveform[:, start:start + self.crop_samples]

        else:

            pad = self.crop_samples - length

            waveform = torch.nn.functional.pad(waveform, (0, pad))

        mel = self.mel_transform(waveform)

        mel = torch.log(mel + 1e-6)

        return mel, label

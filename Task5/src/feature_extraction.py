import librosa
import numpy as np


class FeatureExtraction:
    def __init__(self, audio, sr):
        self.audio = audio
        self.sr = sr

    def generate_magnitude_spectrogram(self):
        self.stft = librosa.stft(
            y=self.audio,
            n_fft=512,
            win_length=400,
            hop_length=160
        )

        self.magnitude = np.abs(self.stft)

        return self.magnitude

    def normalize_features(self):
        mean = np.mean(self.magnitude)
        std = np.std(self.magnitude)

        if std == 0:
            std = 1e-8

        self.magnitude = (self.magnitude - mean) / std

        return self.magnitude

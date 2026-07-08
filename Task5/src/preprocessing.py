import librosa
import numpy as np


class Preprocessing:
    def __init__(self, audio_path):
        self.audio = audio_path

    def load_audio_file(self):
        self.y, self.sr = librosa.load(self.audio, sr=None)

        return self.y, self.sr

    def random_crop(self, crop_duration):
        crop_samples = crop_duration * self.sr
        max_start = len(self.y) - crop_samples
        start = np.random.randint(0, max_start + 1)
        self.y = self.y[start: start + crop_samples]

        return self.y

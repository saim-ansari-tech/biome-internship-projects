import torch
import torch.nn.functional as F
import torchaudio
import torchaudio.transforms as T
import soundfile as sf
import config


mel_transform = T.MelSpectrogram(
    sample_rate=config.SAMPLE_RATE,
    n_fft=config.N_FFT,
    win_length=config.WIN_LENGTH,
    hop_length=config.HOP_LENGTH,
    n_mels=config.N_MELS,
    power=2.0,
)


def preprocess_audio(file_path):

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

    if sample_rate != config.SAMPLE_RATE:
        resampler = T.Resample(sample_rate, config.SAMPLE_RATE)
        waveform = resampler(waveform)
        sample_rate = config.SAMPLE_RATE

    crop_samples = config.CROP_DURATION * config.SAMPLE_RATE
    length = waveform.shape[1]

    if length > crop_samples:
        start = (length - crop_samples) // 2
        waveform = waveform[:, start:start + crop_samples]
    else:
        pad = crop_samples - length
        waveform = F.pad(waveform, (0, pad))

    mel = mel_transform(waveform)
    mel = torch.log(mel + 1e-6)

    return mel

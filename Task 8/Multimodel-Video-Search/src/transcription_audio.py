from pathlib import Path
from faster_whisper import WhisperModel


def transcribe_audio(audio_path: str):
    model = WhisperModel(
        "small",
        device="cuda",
        compute_type="float16"
    )
    audio_path = Path(audio_path)
    print("Model succesfully transcribe the audio")
    segments, info = model.transcribe(audio_path, beam_size=5, language="en")
    transcript = ""
    segment_data = []

    for segment in segments:
        transcript += segment.text.strip() + " "

        segment_data.append(
            {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            }
        )

    print(f"Language: {info.language}")
    print(f"Confidence: {info.language_probability:.2f}")

    return {
        "language": info.language,
        "language_probability": info.language_probability,
        "segments": segment_data
    }

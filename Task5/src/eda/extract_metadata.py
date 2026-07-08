import soundfile as sf
from pathlib import Path
import pandas as pd


def extract_metadata():
    root = Path(
        r"D:\Internship_projects\biome-internship-projects"
        r"\Task5\data\vox1_dev_wav\wav"
    )

    metadata = []

    total_audio = 0

    for audio_file in root.rglob("*.wav"):
        try:
            info = sf.info(audio_file)

            metadata.append({
                "speaker_id": audio_file.parts[-3],
                "video_id": audio_file.parts[-2],
                "audio_file": audio_file.name,
                "file_path": str(audio_file),
                "duration": info.duration,
                "sample_rate": info.samplerate,
                "channels": info.channels,
                "format": info.format,
                "subtype": info.subtype
            })

            total_audio += 1

            if total_audio % 1000 == 0:
                print(f"Processed {total_audio} files...")

        except Exception as e:
            print(f"Error: {audio_file}")
            print(e)

    df = pd.DataFrame(metadata)

    df.to_csv("metadata.csv", index=False)

    print("\nMetadata saved successfully!")
    print(df.head())
    print(f"\nTotal files: {len(df)}")


extract_metadata()

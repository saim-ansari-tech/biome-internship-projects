import os
from pathlib import Path
from audio_extract import extract_audio


def extract_audio_from_video(
    input_path: str,
    output_dir: str,
    output_format: str = "wav"
):
    try:
        video_name = Path(input_path).stem
        output_path = Path(output_dir) / f"{video_name}_audio"

        output_file = f"{output_path}.{output_format}"
        if os.path.exists(output_file):
            os.remove(output_file)

        extract_audio(input_path, str(output_path), output_format)
        audio_file = f"{output_path}.{output_format}"
        print(f'Audio extracted successfully: {audio_file}')
        return audio_file

    except FileNotFoundError:
        raise FileNotFoundError(f"Input video not found: {input_path}")

    except PermissionError:
        raise PermissionError("Permission denied while accessing the file.")

    except Exception as e:
        raise RuntimeError(f"Failed to extract audio: {e}")

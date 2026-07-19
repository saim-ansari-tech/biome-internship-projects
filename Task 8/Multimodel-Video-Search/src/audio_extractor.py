from audio_extract import extract_audio

from audio_extract import extract_audio


def extract_audio_from_video(input_path: str, output_path: str, output_format: str = "wav"):
    try:
        extract_audio(input_path, output_path, output_format)
        print(f"Audio extracted successfully: {output_path}")
        return output_path

    except FileNotFoundError:
        raise FileNotFoundError(f"Input video not found: {input_path}")

    except PermissionError:
        raise PermissionError("Permission denied while accessing the file.")

    except Exception as e:
        raise RuntimeError(f"Failed to extract audio: {e}")



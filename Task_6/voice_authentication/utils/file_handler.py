import os
from werkzeug.utils import secure_filename
import config


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS
    )


def save_uploaded_file(audio_file):

    if audio_file is None or audio_file.filename == "":
        raise ValueError("No file uploaded.")

    if not allowed_file(audio_file.filename):
        raise ValueError("Unsupported file type.")

    filename = secure_filename(audio_file.filename)

    file_path = os.path.join("uploads", filename)

    audio_file.save(file_path)

    return file_path

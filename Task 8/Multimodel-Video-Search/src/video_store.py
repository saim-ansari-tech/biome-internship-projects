import json
from pathlib import Path


DATA_DIR = Path("data/videos")

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def save_video_result(result):

    video_id = result["video_id"]

    video_dir = DATA_DIR / video_id

    video_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    result_path = video_dir / "result.json"

    with open(
        result_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            indent=4,
            ensure_ascii=False
        )

    return str(result_path)


def get_video_result(video_id):

    result_path = (
        DATA_DIR
        / video_id
        / "result.json"
    )

    if not result_path.exists():

        return None

    with open(
        result_path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)

import cv2
from pathlib import Path
from src.scenes_detector import detect_scenes


def extract_frames(video_path: str, output_dir: str):
    scene_list = detect_scenes(video_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception("Could not open video.")

    frames_metadata = []
    for scene_id, scene in enumerate(scene_list, start=1):
        start, end = scene

        start_sec = start.seconds
        end_sec = end.seconds
        middle_sec = (start_sec + end_sec) / 2
        middle_ms = middle_sec * 1000
        cap.set(
            cv2.CAP_PROP_POS_MSEC,
            middle_ms
        )
        success, frame = cap.read()

        if not success:
            continue

        image_path = Path(output_dir) / f"scene_{scene_id:03d}.jpg"

        cv2.imwrite(str(image_path), frame)

        frames_metadata.append(
            {
                "scene_id": scene_id,
                "timestamp": middle_sec,
                "image_path": str(image_path)
            }
        )

    cap.release()
    return frames_metadata

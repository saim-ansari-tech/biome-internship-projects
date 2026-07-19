from pipeline import process_video

VIDEO_PATH = r"D:\Internship\biome-internship-projects\Task 8\Multimodel-Video-Search\data\audio\video.mp4"
KEYFRAME_OUTPUT_DIR = r"D:\Internship\biome-internship-projects\Task 8\Multimodel-Video-Search\data\keyframes"

result = process_video(
    video_path=VIDEO_PATH,
    keyframe_output_dir=KEYFRAME_OUTPUT_DIR
)


print("VIDEO SUMMARY")


print(result["summary"]["summary"])


print("CHAPTERS")

for chapter in result["summary"]["chapters"]:
    print(
        f"{chapter['start_time']} - {chapter['title']}"
    )
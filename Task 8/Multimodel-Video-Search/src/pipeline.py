from pathlib import Path

from src.scenes_detector import detect_scenes
from src.frames_extractor import extract_frames
from src.audio_extractor import extract_audio_from_video
from src.scene_description import generate_scene_description

from src.transcription_audio import transcribe_audio
from src.summary_generator import generate_summary

from src.text_chunker import chunk_transcript
from src.embedding_generator import generate_embeddings

from src.vector_store import (
    create_collection,
    store_chunks,
)


def process_video(video_path: str, keyframe_output_dir: str, video_id: str):
    print("Starting Video Processing Pipeline...\n")
    print(f"Video ID: {video_id}")

    print("\nDetecting scenes...")
    scene_list = detect_scenes(video_path)
    print(f"Detected {len(scene_list)} scenes.")

    print("\nExtracting keyframes...")
    frames_metadata = extract_frames(video_path, keyframe_output_dir)

    print("\nGenerating scene descriptions...")
    frames_metadata = generate_scene_description(frames_metadata)

    print("\nExtracting audio...")
    AUDIO_DIR = Path("data/audio")
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    audio_path = extract_audio_from_video(video_path, str(AUDIO_DIR))
    print(f"Audio file path: {audio_path}")

    print("\nTranscribing audio...")
    transcription = transcribe_audio(audio_path)

    print("\n" + "=" * 60)
    print("TRANSCRIPT")
    print("=" * 60)
    for segment in transcription["segments"]:
        print(
            f"[{segment['start']:.2f}s - {segment['end']:.2f}s]"
            f"{segment['text']}"
        )

    transcript_text = " ".join(
        segment["text"]
        for segment in transcription["segments"]
    )

    print("\nGenerating summary...")
    summary_result = generate_summary(
        transcript=transcript_text,
        scenes_metadata=frames_metadata
    )

    print("\n" + "=" * 60)
    print("VIDEO SUMMARY")
    print("=" * 60)
    print(summary_result["summary"])

    print("\n" + "=" * 60)
    print("CHAPTERS")
    print("=" * 60)
    for chapter in summary_result["chapters"]:
        print(f"\n{chapter['title']}")
        print(f"Start: {chapter['start_time']:.2f}s")
        print(f"{chapter['description']}")

    print("\nChunking transcript...")
    chunks = chunk_transcript(transcription["segments"], video_id=video_id)

    print("\nGenerating embeddings...")
    embedded_chunks = generate_embeddings(chunks)

    print("\nStoring vectors...")
    create_collection()
    store_chunks(embedded_chunks)

    print("\nPipeline Completed Successfully!")

    result = {
        "video_id": video_id,
        "transcript": transcription,
        "summary": summary_result,
        "scenes_metadata": frames_metadata,
        "chunks": chunks
    }
    return result

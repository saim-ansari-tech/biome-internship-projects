from pathlib import Path

from scenes_detector import detect_scenes
from frames_extractor import extract_frames
from scene_description import generate_scene_description

from transcription_audio import transcribe_audio
from summary_generator import generate_summary

from text_chunker import chunk_transcript
from embedding_generator import generate_embeddings

from vector_store import (
    create_collection,
    store_chunks,
)

def process_video(video_path: str, keyframe_output_dir: str):
    print("Starting Video Processing Pipeline... \n")

    print("\nDetecting scenes...")

    scene_list = detect_scenes(video_path)
     
    print(f"Detected {len(scene_list)} scenes.")

    print("\nExtracting keyframes...")

    frames_metadata = extract_frames(
        video_path,
        keyframe_output_dir
    )

    print("\nGenerating scene descriptions...")

    frames_metadata = generate_scene_description(
        frames_metadata
    )

    print("\nTranscribing audio...")

    transcription = transcribe_audio(video_path)

    print("\nGenerating summary...")

    summary = generate_summary(
        transcript=transcription,
        scene_metadata=frames_metadata
    )

    print("\nChunking transcript...")

    chunks = chunk_transcript(
        transcription
    )

    print("\nGenerating embeddings...")

    embedded_chunks = generate_embeddings(
        chunks
    )

    print("\nStoring vectors...")

    create_collection()

    store_chunks(
        embedded_chunks
    )

    print("\nPipeline Completed Successfully!")

    return {
        "summary": summary,
        "scene_metadata": frames_metadata,
        "chunks": chunks,
    }


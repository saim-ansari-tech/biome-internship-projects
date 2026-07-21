import os
import json
import uuid
import threading
from pathlib import Path

from flask import (
    Flask,
    request,
    jsonify,
    render_template
)
from flask_cors import CORS

from src.video_store import save_video_result, get_video_result, DATA_DIR
from src.question_answering import answer_question

app = Flask(__name__)
CORS(app)

UPLOAD_DIR = Path("data/uploads")
KEYFRAME_DIR = Path("data/keyframes")
PROCESSING_STATUS = {}

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
KEYFRAME_DIR.mkdir(parents=True, exist_ok=True)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/processing", methods=["GET"])
def processing_page():
    return render_template("processing.html")


@app.route("/results", methods=["GET"])
def results_page():
    return render_template("results.html")


@app.route("/search", methods=["GET"])
def search_page():
    return render_template("search.html")


@app.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({
            "success": False,
            "error": "No video file provided."
        }), 400

    video = request.files["video"]
    if video.filename == "":
        return jsonify({"success": False, "error": "No video selected."}), 400

    video_id = str(uuid.uuid4())
    extension = Path(video.filename).suffix
    video_path = UPLOAD_DIR / f"{video_id}{extension}"
    video.save(video_path)

    keyframe_dir = KEYFRAME_DIR / video_id
    keyframe_dir.mkdir(parents=True, exist_ok=True)

    PROCESSING_STATUS[video_id] = {
        "status": "processing",
        "progress": 5,
        "error": None,
        "step": "Initializing",
        "metadata": {
            "fileName": video.filename,
            "size": os.path.getsize(video_path),
            "uploadTime": str(Path(video_path).stat().st_mtime)
        }
    }

    thread = threading.Thread(
        target=_process_video_async,
        args=(str(video_path), str(keyframe_dir), video_id)
    )
    thread.daemon = True
    thread.start()

    return jsonify({
        "success": True,
        "video_id": video_id,
        "message": "Video uploaded. Processing started in background.",
        "status": "processing"
    })


def _update_status(video_id, progress, step, metadata=None):
    """Update processing status with progress info."""
    if video_id in PROCESSING_STATUS:
        PROCESSING_STATUS[video_id]["progress"] = progress
        PROCESSING_STATUS[video_id]["step"] = step
        if metadata:
            PROCESSING_STATUS[video_id]["metadata"].update(metadata)


def _process_video_async(video_path, keyframe_dir, video_id):
    """Background processing with step-by-step progress updates."""
    try:
        _update_status(video_id, 5, "Upload Complete")

        _update_status(video_id, 10, "Scene Detection")

        result = _run_pipeline_with_progress(
            video_path,
            keyframe_dir,
            video_id
        )

        result["video_filename"] = os.path.basename(video_path)
        result["video_path"] = str(video_path)
        save_video_result(result)

        PROCESSING_STATUS[video_id] = {
            "status": "completed",
            "progress": 100,
            "error": None,
            "video_id": video_id,
            "step": "Complete",
            "metadata": {
                "fileName": result.get("video_filename", "Unknown"),
                "duration": result.get("duration", "--"),
                "scenes": len(result.get("scenes_metadata", [])),
                "transcriptLength":
                len(result.get("transcript", {}).get("segments", [])),
                "chunks": len(result.get("chunks", []))
            }
        }

    except Exception as e:
        import traceback
        error_msg = str(e)
        print(f"Processing failed for {video_id}: {error_msg}")
        print(traceback.format_exc())
        PROCESSING_STATUS[video_id] = {
            "status": "failed",
            "progress": 0,
            "error": error_msg,
            "step": "Failed",
            "metadata": {}
        }


def _run_pipeline_with_progress(video_path, keyframe_dir, video_id):
    """Run pipeline and update progress at each step."""
    from src.scenes_detector import detect_scenes
    from src.frames_extractor import extract_frames
    from src.audio_extractor import extract_audio_from_video
    from src.scene_description import generate_scene_description
    from src.transcription_audio import transcribe_audio
    from src.summary_generator import generate_summary
    from src.text_chunker import chunk_transcript
    from src.embedding_generator import generate_embeddings
    from src.vector_store import create_collection, store_chunks
    from pathlib import Path

    print(f"Starting Video Processing Pipeline...\nVideo ID: {video_id}")

    _update_status(video_id, 10, "Scene Detection")
    scene_list = detect_scenes(video_path)
    _update_status(
        video_id, 15,
        "Scene Detection",
        {"scenes": len(scene_list)})
    print(f"Detected {len(scene_list)} scenes.")

    _update_status(video_id, 20, "Keyframe Extraction")
    frames_metadata = extract_frames(video_path, keyframe_dir)
    _update_status(
        video_id, 25,
        "Keyframe Extraction",
        {"frames": len(frames_metadata)})
    print(f"Extracted {len(frames_metadata)} keyframes.")

    _update_status(video_id, 30, "Scene Description (VLM)")
    frames_metadata = generate_scene_description(frames_metadata)
    _update_status(video_id, 40, "Scene Description Complete")

    _update_status(video_id, 45, "Audio Extraction")
    AUDIO_DIR = Path("data/audio") / video_id
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    audio_path = extract_audio_from_video(video_path, str(AUDIO_DIR))
    _update_status(video_id, 50, "Audio Extraction Complete")
    print(f"Audio extracted: {audio_path}")

    _update_status(video_id, 55, "Transcribing (Whisper)")
    transcription = transcribe_audio(audio_path)
    _update_status(video_id, 65, "Transcription Complete", {
        "transcriptLength": len(transcription.get("segments", [])),
        "language": transcription.get("language", "en")
    })
    print(f"Transcribed {len(transcription['segments'])} segments.")

    transcript_text = " ".join(segment["text"]
                               for segment in
                               transcription["segments"])

    _update_status(video_id, 70, "Generating Summary & Chapters")
    summary_result = generate_summary(
        transcript=transcript_text,
        scenes_metadata=frames_metadata
    )
    _update_status(video_id, 80, "Summary Complete")

    _update_status(video_id, 85, "Chunking Transcript")
    chunks = chunk_transcript(transcription["segments"], video_id=video_id)

    _update_status(video_id, 90, "Generating Embeddings")
    embedded_chunks = generate_embeddings(chunks)

    _update_status(video_id, 95, "Storing in Qdrant")
    create_collection()
    store_chunks(embedded_chunks)

    _update_status(video_id, 98, "Finalizing")

    print("\nPipeline Completed Successfully!")

    return {
        "video_id": video_id,
        "transcript": transcription,
        "summary": summary_result,
        "scenes_metadata": frames_metadata,
        "chunks": chunks
    }


@app.route("/status/<video_id>", methods=["GET"])
def get_status(video_id):
    """Poll this endpoint to check processing progress."""
    status = PROCESSING_STATUS.get(video_id)
    if not status:
        result = get_video_result(video_id)
        if result:
            return jsonify({
                "success": True,
                "status": "completed",
                "progress": 100,
                "video_id": video_id,
                "step": "Complete",
                "metadata": {
                    "fileName": result.get("video_filename", "Unknown"),
                    "scenes": len(result.get("scenes_metadata", [])),
                    "transcriptLength":
                    len(result.get("transcript", {}).get("segments", []))
                }
            })
        return jsonify({"success": False, "error": "Video ID not found."}), 404

    return jsonify({"success": True, **status})


@app.route("/video/<video_id>", methods=["GET"])
def get_video(video_id):
    result = get_video_result(video_id)
    if result is None:
        return jsonify({"success": False, "error": "Video not found."}), 404

    video_path = result.get("video_path", "")
    if video_path and os.path.exists(video_path):
        # Return a relative URL that Flask can serve
        result["video_url"] = f"/video_file/{video_id}"

    return jsonify({"success": True, "video": result})


@app.route("/video_file/<video_id>", methods=["GET"])
def serve_video_file(video_id):
    """Serve the actual video file for playback."""
    result = get_video_result(video_id)
    if not result:
        return jsonify({"success": False, "error": "Video not found"}), 404

    video_path = result.get("video_path", "")
    if not video_path or not os.path.exists(video_path):
        return jsonify({
            "success": False,
            "error": "Video file not found"
            }), 404

    from flask import send_file
    return send_file(video_path, mimetype='video/mp4')


@app.route("/ask", methods=["POST"])
def ask_question_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "error": "Request body is required."
        }), 400

    video_id = data.get("video_id")
    question = data.get("question")
    top_k = data.get("top_k", 5)

    if not video_id:
        return jsonify({
            "success": False,
            "error": "video_id is required."
        }), 400
    if not question:
        return jsonify({
            "success": False,
            "error": "question is required."
        }), 400

    try:
        result = get_video_result(video_id)
        if not result:
            return jsonify({
                "success": False,
                "error": "Video not found or not processed yet."
                }), 404

        result = answer_question(
            question=question,
            video_id=video_id,
            top_k=top_k,
            similarity_threshold=0.15  # Lowered from 0.20
        )

        return jsonify({
            "success": True,
            "video_id": video_id,
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"]
        })

    except Exception as e:
        import traceback
        print(f"Ask question error: {e}")
        print(traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/videos", methods=["GET"])
def list_videos():
    """List all processed videos for the dashboard."""
    videos = []
    if DATA_DIR.exists():
        for video_dir in DATA_DIR.iterdir():
            if video_dir.is_dir():
                result_file = video_dir / "result.json"
                if result_file.exists():
                    with open(result_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        # Clean up summary for display
                        summary_text = ""
                        if isinstance(data.get("summary"), dict):
                            summary_text = (
                                data["summary"].get("summary", "")[:200]
                            )
                        elif isinstance(data.get("summary"), str):
                            summary_text = data["summary"][:200]
                        videos.append({
                            "video_id": data.get("video_id"),
                            "video_filename":
                            data.get("video_filename", "Unknown"),
                            "summary": summary_text + "..."
                            if summary_text else "No summary"
                        })
    return jsonify({"success": True, "videos": videos})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

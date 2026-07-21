def chunk_transcript(
    segments: list,
    video_id: str,
    max_words: int = 150
):

    chunks = []

    chunk_text = []
    chunk_words = 0
    chunk_start = None
    chunk_end = None

    chunk_id = 1

    for segment in segments:

        text = segment["text"].strip()
        words = len(text.split())

        if chunk_start is None:
            chunk_start = segment["start"]

        chunk_text.append(text)
        chunk_words += words
        chunk_end = segment["end"]

        # Finish chunk only AFTER adding a complete Whisper segment
        if chunk_words >= max_words:

            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "video_id": video_id,
                    "start_time": chunk_start,
                    "end_time": chunk_end,
                    "text": " ".join(chunk_text)
                }
            )

            chunk_id += 1

            chunk_text = []
            chunk_words = 0
            chunk_start = None
            chunk_end = None

    # Last chunk
    if chunk_text:

        chunks.append(
            {
                "chunk_id": chunk_id,
                "video_id": video_id,
                "start_time": chunk_start,
                "end_time": chunk_end,
                "text": " ".join(chunk_text)
            }
        )

    return chunks

from vector_store import search

def search_video(query, top_k=3):

    results = search(query, top_k)

    retrieved_chunks = []

    for result in results:

        retrieved_chunks.append(
            {
                "score": result.score,
                "text": result.payload["text"],
                "start_time": result.payload["start_time"],
                "end_time": result.payload["end_time"],
            }
        )

    return retrieved_chunks

from src.vector_store import search
from src.llm_generator import generate_answer


def answer_question(
    question: str,
    video_id: str,
    top_k: int = 3,
    similarity_threshold: float = 0.20
):

    results = search(
        query=question,
        video_id=video_id,
        top_k=top_k
    )

    if not results.points:

        return {
            "answer": "Sorry, I cannot find this information in the video.",
            "sources": []
        }

    relevant_points = [

        point

        for point in results.points

        if point.score >= similarity_threshold

    ]

    if not relevant_points:

        return {
            "answer": "Sorry, I cannot find this information in the video.",
            "sources": []
        }

    context_parts = []
    sources = []

    for point in relevant_points:

        payload = point.payload

        context_parts.append(
            payload["text"]
        )

        sources.append(
            {
                "start_time": payload["start_time"],
                "end_time": payload["end_time"],
                "text": payload["text"],
                "score": point.score
            }
        )

    context = "\n\n".join(
        context_parts
    )

    answer = generate_answer(
        question=question,
        context=context
    )

    return {
        "answer": answer,
        "sources": sources
    }

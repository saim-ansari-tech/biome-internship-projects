def semantic_search(
    vector_store,
    query: str,
    top_k: int = 3
):
    results = vector_store.similarity_search_with_score(
        query=query,
        k=top_k
    )

    return results

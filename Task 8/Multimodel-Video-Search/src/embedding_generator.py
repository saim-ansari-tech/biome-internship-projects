from sentence_transformers import SentenceTransformer


def generate_embeddings(chunks):

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    embedded_chunks = []

    for chunk in chunks:

        embedding = model.encode(
            chunk["text"],
            convert_to_numpy=True
        )

        embedded_chunks.append(
            {
                **chunk,
                "embedding": embedding.tolist()
            }
        )

    return embedded_chunks

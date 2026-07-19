from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

client = QdrantClient(
    url="http://localhost:6333"
)

def create_collection():
    collections = client.get_collections().collections

    collection_names = [
        c.name for c in collections
    ]

    if "multimodal" not in collection_names:

        client.create_collection(
            collection_name="multimodal",
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

        print("Collection Created.")

    else:

        print("Collection Already Exists.")


def store_chunks(embedded_chunks):

    points = []

    for chunk in embedded_chunks:

        points.append(

            PointStruct(

                id=chunk["chunk_id"],

                vector=chunk["embedding"],

                payload={

                    "text": chunk["text"],

                    "start_time": chunk["start_time"],

                    "end_time": chunk["end_time"]

                }

            )

        )

    client.upsert(
        collection_name="multimodal",
        points=points
    )

    print(f"{len(points)} chunks inserted.")


def search(query, top_k=3):

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = client.search(
        collection_name="multimodal",
        query_vector=query_embedding,
        limit=top_k
    )

    return results
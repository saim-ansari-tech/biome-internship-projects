import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
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

                id=str(uuid.uuid4()),

                vector=chunk["embedding"],

                payload={

                    "video_id": chunk["video_id"],

                    "chunk_id": chunk["chunk_id"],

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


def search(query, video_id, top_k=3):

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = client.query_points(
        collection_name="multimodal",
        query=query_embedding,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="video_id",
                    match=MatchValue(
                        value=video_id
                    )
                )
            ]
        ),
        limit=top_k
    )

    return results

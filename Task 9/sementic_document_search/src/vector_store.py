from langchain_huggingface import (
    HuggingFaceEmbeddings
)
from langchain_qdrant import (
    QdrantVectorStore
)

COLLECTION_NAME = (
    "semantic_documents"
)

QDRANT_URL = (
    "http://localhost:6333"
)


def get_embeddings():

    return HuggingFaceEmbeddings(

        model_name=(
            "sentence-transformers/"
            "all-MiniLM-L6-v2"
        )

    )


def create_vector_store(chunks):

    embeddings = get_embeddings()

    vector_store = (
        QdrantVectorStore.from_documents(

            documents=chunks,

            embedding=embeddings,

            url=QDRANT_URL,

            collection_name=(
                COLLECTION_NAME
            )

        )
    )

    return vector_store


def get_vector_store():

    embeddings = get_embeddings()

    vector_store = (
        QdrantVectorStore.from_existing_collection(

            embedding=embeddings,

            collection_name=(
                COLLECTION_NAME
            ),

            url=QDRANT_URL

        )
    )

    return vector_store

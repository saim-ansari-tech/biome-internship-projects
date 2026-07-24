from pathlib import Path
from src.document_loader import load_corpus
from src.document_splitter import text_splitter
from src.vector_store import create_vector_store
from src.sementic_search import semantic_search


def main():

    document_director = Path(
        r"D:\Internship_projects\biome-internship-projects"
        r"\Task 9\sementic_document_search\data\documents"
    )

    document = load_corpus(document_director)

    chunks = text_splitter(document)

    vector_store = create_vector_store(chunks)

    query = "What is Natural Language Processing?"

    results = semantic_search(vector_store, query)

    print(f"\nQuery: {query}")
    print(f"Retrieved {len(results)} chunks\n")

    for rank, (document, score) in enumerate(results, start=1):

        print("=" * 80)
        print(f"Rank: {rank}")
        print(f"Similarity Score: {score:.4f}")
        print(f"Source: {document.metadata.get('source')}")
        print(f"Content:\n{document.page_content}")


main()

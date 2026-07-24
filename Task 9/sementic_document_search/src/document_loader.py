from pathlib import Path
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader
)


def text_loader(file_path: Path):
    loader = TextLoader(
        file_path,
        encoding="utf-8"
    )

    return loader.load()


def pdf_loader(file_path: Path):
    loader = PyPDFLoader(file_path)

    return loader.load()


def doc_loader(file_path: Path):
    loader = Docx2txtLoader(file_path)

    return loader.load()


def load_document(file_path: Path):

    file_type = file_path.suffix.lower()

    if file_type == ".txt":
        return text_loader(file_path)

    elif file_type == ".pdf":
        return pdf_loader(file_path)

    elif file_type == ".docx":
        return doc_loader(file_path)

    else:
        raise ValueError(
            f"Unsupported file type: {file_type}"
        )


def load_corpus(directory: Path):

    documents = []

    for file_path in directory.iterdir():

        if not file_path.is_file():
            continue

        try:

            loaded_documents = load_document(
                file_path
            )

            for document in loaded_documents:

                document.metadata["file_name"] = (
                    file_path.name
                )

                document.metadata["file_type"] = (
                    file_path.suffix.lower()
                )

            documents.extend(
                loaded_documents
            )

            print(
                f"Loaded: {file_path.name}"
            )

        except ValueError as error:

            print(
                f"Skipped: {file_path.name} "
                f"→ {error}"
            )

    return documents

from langchain_text_splitters import RecursiveCharacterTextSplitter


def text_splitter(document: list,
                  chunk_size: int = 500,
                  overlap_size: int = 50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap_size
    )
    chunks = splitter.split_documents(document)

    return chunks


import hashlib

from services.embedding_service import generate_embeddings
from services.vector_store import store_documents


def generate_document_id(source: str) -> str:
    return hashlib.sha256(
        source.encode("utf-8")
    ).hexdigest()


def split_into_chunks(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100
) -> list[str]:
    """
    Split text into overlapping character chunks.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and < chunk_size")

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


async def ingest_document(
    title: str,
    content: str
):
    """
    Split, embed and store a document.
    """

    if not content.strip():
        raise ValueError("Document content cannot be empty")

    document_id = generate_document_id(
        title + content
    )

    chunks = split_into_chunks(content)

    embeddings = await generate_embeddings(chunks)

    ids = [
        f"{document_id}_{index}"
        for index in range(len(chunks))
    ]

    metadatas = [
        {
            "document_id": document_id,
            "title": title,
            "chunk_index": index
        }
        for index in range(len(chunks))
    ]

    store_documents(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return {
        "document_id": document_id,
        "title": title,
        "chunks_created": len(chunks)
    }

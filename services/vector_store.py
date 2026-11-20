
import chromadb
from pathlib import Path


DB_PATH = Path("data/chroma_db")

client = chromadb.PersistentClient(
    path=str(DB_PATH)
)

collection = client.get_or_create_collection(
    name="enterprise_knowledge",
    metadata={"hnsw:space": "cosine"}
)


def store_documents(
    ids: list[str],
    documents: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict]
):
    """
    Store document chunks and their embeddings.
    """

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )


def search_documents(
    query_embedding: list[float],
    top_k: int = 5
):
    """
    Retrieve the most similar document chunks.
    """

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

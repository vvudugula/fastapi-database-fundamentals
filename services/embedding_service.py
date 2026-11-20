
import httpx
from typing import List


OLLAMA_URL = "http://localhost:11434/api/embed"
EMBEDDING_MODEL = "nomic-embed-text"


async def generate_embeddings(
    texts: List[str]
) -> List[List[float]]:
    """
    Generate embeddings for a list of texts using Ollama.
    """

    if not texts:
        raise ValueError("Input texts cannot be empty")

    payload = {
        "model": EMBEDDING_MODEL,
        "input": texts
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            OLLAMA_URL,
            json=payload
        )

        response.raise_for_status()

        result = response.json()

    embeddings = result.get("embeddings")

    if not embeddings:
        raise ValueError("Ollama returned no embeddings")

    if len(embeddings) != len(texts):
        raise ValueError("Embedding count does not match input count")

    return embeddings

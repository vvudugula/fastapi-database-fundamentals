
import httpx

from schemas.semantic_search import SearchRequest
from services.embedding_service import generate_embeddings
from services.vector_store import search_documents


OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "qwen2.5:3b"


async def generate_rag_answer(
    question: str,
    top_k: int = 3,
):
    # 1. Generate the question embedding

    # TODO: Call generate_embeddings()
    query_embeddings = await generate_embeddings(
                [question]
            )

    # 2. Retrieve relevant chunks from ChromaDB

    # TODO: Call search_documents()
    results = search_documents(
                query_embedding=query_embeddings[0],
                top_k=top_k
            )

    # 3. Prepare context from retrieved documents
    matches = []
    
    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        matches.append({
            "content": document,
            "title": metadata.get("title"),
            "chunk_index": metadata.get("chunk_index"),
            "distance": round(distance, 4)
        })
    # TODO: Combine retrieved chunks into context
    context = "\n\n".join(
        [
            f"Source: {match['title']}\n"
            f"Content: {match['content']}"
            for match in matches
        ]
    )

    # 4. Build the prompt

    # TODO: Include context and user question
    # Tell the LLM to answer only using supplied context.
    prompt = f"""
        You are an enterprise knowledge assistant.

        Answer the user's question using ONLY the context provided below.

        Rules:
        1. Do not invent information.
        2. If the context does not contain the answer, say:
        "I don't have enough information in the provided documents."
        3. Keep the answer clear and concise.

        CONTEXT:
        {context}

        USER QUESTION:
        {question}

        ANSWER:
        """

    # 5. Call the local Qwen model

    # TODO: Use httpx.AsyncClient
    # POST to OLLAMA_GENERATE_URL
    # Use stream=False
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            OLLAMA_GENERATE_URL,
            json={
                "model": LLM_MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

    response.raise_for_status()

    result = response.json()

    answer = result["response"]

    # 6. Return answer and source documents

    # TODO: Return the generated answer and source metadata
    return {
        "question": question,
        "answer": answer,
        "sources": matches
    }
    #pass

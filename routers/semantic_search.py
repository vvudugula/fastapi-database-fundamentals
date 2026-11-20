
from fastapi import APIRouter, HTTPException

from schemas.semantic_search import (
    DocumentRequest,
    SearchRequest,
    IngestionResponse
)

from services.document_service import ingest_document
from services.embedding_service import generate_embeddings
from services.vector_store import search_documents


router = APIRouter(
    prefix="/semantic-search",
    tags=["Semantic Search"]
)


@router.post("/ingest", response_model=IngestionResponse)
async def ingest(request: DocumentRequest):

    try:
        result = await ingest_document(
            title=request.title,
            content=request.content
        )

        return result

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Document ingestion failed: {str(exc)}"
        )


@router.post("/search")
async def search(request: SearchRequest):

    try:
        query_embeddings = await generate_embeddings(
            [request.query]
        )

        results = search_documents(
            query_embedding=query_embeddings[0],
            top_k=request.top_k
        )

        matches = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):
            matches.append({
                "content": document,
                "metadata": metadata,
                "distance": distance
            })

        return {
            "query": request.query,
            "results_count": len(matches),
            "results": matches
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Semantic search failed: {str(exc)}"
        )


@router.post("/searchv")
async def search(request: SearchRequest):

    try:
        query_embeddings = await generate_embeddings(
            [request.query]
        )

        results = search_documents(
            query_embedding=query_embeddings[0],
            top_k=request.top_k
        )

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

        return {
            "query": request.query,
            "results_count": len(matches),
            "results": matches
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Semantic search failed"
        )

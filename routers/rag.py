
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.rag_service import generate_rag_answer

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)


class RAGRequest(BaseModel):
    question: str = Field(min_length=3)
    top_k: int = Field(default=3, ge=1, le=10)


@router.post("/ask")
async def ask_question(request: RAGRequest):

    try:
        result = await generate_rag_answer(
            question=request.question,
            top_k=request.top_k
        )

        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to process RAG request"
        )

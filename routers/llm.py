from fastapi import APIRouter, HTTPException
import httpx

from schemas.llm import LLMRequest, LLMResponse
from services.ollama_service import (
    generate_response,
    MODEL_NAME
)

router = APIRouter(
    prefix="/llm",
    tags=["LLM"]
)


@router.post("/generate", response_model=LLMResponse)
async def generate(request: LLMRequest):

    try:
        answer = await generate_response(
            request.prompt,
            request.temperature
        )

        return LLMResponse(
            prompt=request.prompt,
            response=answer,
            model=MODEL_NAME
        )

    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Ollama service is unavailable"
        )

    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=502,
            detail="Ollama returned an unsuccessful response"
        )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="LLM generation timed out"
        )
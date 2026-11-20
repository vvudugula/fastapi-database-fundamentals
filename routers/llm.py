from fastapi import APIRouter, HTTPException
import httpx

from schemas.llm import LLMRequest, LLMResponse
from services.ollama_service import (
    generate_response,
    generate_response_java,
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
            system_prompt=request.system_prompt,
            prompt=request.prompt,
            temperature=request.temperature,
            response_format=request.response_format,
            max_token=request.max_token
        )
        print(answer)
        total = answer.get("tokens_used").get("total_tokens")
        return LLMResponse(
            prompt=request.prompt,
            response=answer["response"],  # Extract the text string from the dict
            model=MODEL_NAME,
            tokens=total
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

@router.post("/technical-assistant", response_model=LLMResponse)
async def generate(request: LLMRequest):

    try:
        answer = await generate_response_java(
            prompt=request.prompt,
            temperature=request.temperature,
            response_format=request.response_format
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

@router.post("/rag", response_model=LLMResponse)
async def generate(request: LLMRequest):

    try:
        answer = await generate_response_java(
            prompt=request.prompt,
            temperature=request.temperature,
            response_format=request.response_format
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


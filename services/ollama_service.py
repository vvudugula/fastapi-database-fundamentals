import httpx

OLLAMA_URL = "http://127.0.0.1:11434"
MODEL_NAME = "qwen2.5:3b"


async def generate_response(
    system_prompt: str | None,
    prompt: str,
    temperature: float,
    response_format: str,
    max_token: int
) -> str:

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_token
        }

    }

    if response_format == "json":
        payload["format"] = "json"

    async with httpx.AsyncClient(timeout=180.0) as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/chat",
            json=payload
        )

        response.raise_for_status()

        result = response.json()
        prompt_tokens = result.get("prompt_eval_count", 0)
        generated_tokens = result.get("eval_count", 0)

        return {
            "response": result["message"]["content"],
            "tokens_used": {
                "prompt_tokens": prompt_tokens,
                "generated_tokens": generated_tokens,
                "total_tokens": prompt_tokens + generated_tokens,
            }
        }

async def generate_response_java(
    prompt: str,
    temperature: float,
    response_format: str
) -> str:

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": "You are a senior Java architect with 15 years of enterprise experience. Explain concepts using practical examples."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }

    if response_format == "json":
        payload["format"] = "json"

    async with httpx.AsyncClient(timeout=180.0) as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/chat",
            json=payload
        )

        response.raise_for_status()

        result = response.json()

        return result["message"]["content"]

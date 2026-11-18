import httpx

OLLAMA_URL = "http://127.0.0.1:11434"
MODEL_NAME = "qwen2.5-coder:3b"


async def generate_response(
    prompt: str,
    temperature: float
) -> str:

    payload = {
        "model": MODEL_NAME,
        "messages": [
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

    async with httpx.AsyncClient(timeout=180.0) as client:

        response = await client.post(
            f"{OLLAMA_URL}/api/chat",
            json=payload
        )

        response.raise_for_status()

        result = response.json()

        return result["message"]["content"]
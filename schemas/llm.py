from pydantic import BaseModel, Field
from typing import Literal

from typing import Literal
from pydantic import BaseModel, Field


class LLMRequest(BaseModel):
    system_prompt: str = Field(
        default="You are a helpful AI assistant.",
        max_length=2000,
    )

    prompt: str = Field(
        min_length=1,
        max_length=4000
    )

    temperature: float = Field(
        default=0.3,
        ge=0,
        le=2
    )

    response_format: Literal["text", "json"] = "text"
    max_token: int = Field(
        default = 10000
    )

class LLMResponse(BaseModel):
    prompt: str
    response: str
    model: str
    tokens: int
from pydantic import BaseModel, Field


class LLMRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    temperature: float = Field(default=0.3, ge=0, le=2)


class LLMResponse(BaseModel):
    prompt: str
    response: str
    model: str
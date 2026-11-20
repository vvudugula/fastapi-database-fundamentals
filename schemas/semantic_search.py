
from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    title: str
    content: str


class SearchRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=20)


class IngestionResponse(BaseModel):
    document_id: str
    title: str
    chunks_created: int

from pydantic import BaseModel
from typing import List, Optional, Any
from enum import Enum

class ModalityType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    PDF = "pdf"

class Document(BaseModel):
    id: str
    content: str
    modality: ModalityType
    metadata: dict[str, Any]
    embedding: Optional[List[float]] = None

class QueryRequest(BaseModel):
    query_text: str
    image_url: Optional[str] = None
    top_k: int = 5

class QueryResponse(BaseModel):
    answer: str
    sources: List[Document]

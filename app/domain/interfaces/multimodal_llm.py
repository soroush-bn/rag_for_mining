from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import Document

class MultimodalLLMInterface(ABC):
    """
    Abstract Interface for the Large Language Model.
    Defined in the Domain layer, implemented by the Infrastructure layer.
    """

    @abstractmethod
    async def generate_answer(self, query: str, context: List[Document], image_url: Optional[str] = None) -> str:
        pass

    @abstractmethod
    async def generate_embedding(self, text: str) -> List[float]:
        pass
    
    @abstractmethod
    async def extract_image_features(self, image_bytes: bytes) -> List[float]:
        pass

    @abstractmethod
    async def generate_text_summaries(texts, tables, summarize_texts=False) -> tuple[list[str], list[str]]:
        pass

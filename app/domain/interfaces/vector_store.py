from abc import ABC, abstractmethod
from typing import List, Optional, Any
from app.domain.models import Document

class VectorStoreInterface(ABC):
    """
    Abstract Interface for the Vector Database.
    Defined in the Domain layer, implemented by the Infrastructure layer.
    """

    @abstractmethod
    async def add_documents(self, documents: List[Document]) -> None:
        pass

    @abstractmethod
    async def search(self, query: str, top_k: int) -> List[Document]:
        pass

    @abstractmethod
    async def search_multimodal(self, query: str, image_features: Optional[List[float]], top_k: int) -> List[Document]:
        pass
        
    @abstractmethod
    def get_retriever(self) -> Any:
        pass

    @abstractmethod
    def add_summaries_and_docs(self, doc_summaries: List[str], doc_contents: List[str], batch_size: int = 100) -> None:
        pass

import os
from typing import List, Optional, Any
import uuid
from app.common.constants import PROJECT_ID, REGION
from app.domain.interfaces.vector_store import VectorStoreInterface
from app.domain.models import Document as DomainDocument
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document as LangchainDocument
from langchain_google_vertexai import VertexAIEmbeddings

class PineconeDBImpl(VectorStoreInterface):
    """
    Concrete implementation of the VectorStoreInterface using Pinecone.
    """
    def __init__(self):
        # Initialize Embeddings
        self.embeddings = VertexAIEmbeddings(
            model_name="gemini-embedding-001", 
            project=PROJECT_ID, 
            location=REGION
        )
        
        # Initialize Pinecone
        self.index_name = os.environ.get("PINECONE_INDEX_NAME", "mining-rag")
        self.vectorstore = PineconeVectorStore(
            index_name=self.index_name, 
            embedding=self.embeddings,
            pinecone_api_key=os.environ.get("PINECONE_API_KEY")
        )

    def get_retriever(self) -> Any:
        return self.vectorstore.as_retriever()

    async def add_documents(self, documents: List[DomainDocument]) -> None:
        # Implementation for adding domain documents if needed
        pass

    async def search(self, query: str, top_k: int) -> List[DomainDocument]:
        return self.vectorstore.similarity_search(query, k=top_k)

    async def search_multimodal(self, query: str, image_features: Optional[List[float]], top_k: int) -> List[DomainDocument]:
        # Pinecone multimodal search logic would go here
        pass
    
    def add_summaries_and_docs(self, doc_summaries: List[str], doc_contents: List[str], batch_size: int = 100):
        """
        Adds summaries to Pinecone. 
        """
        for i in range(0, len(doc_summaries), batch_size):
            batch_summaries = doc_summaries[i:i + batch_size]
            batch_contents = doc_contents[i:i + batch_size]
            
            docs = [
                LangchainDocument(
                    page_content=s, 
                    metadata={"full_text": batch_contents[j], "id": str(uuid.uuid4())}
                )
                for j, s in enumerate(batch_summaries)
            ]
            self.vectorstore.add_documents(docs)

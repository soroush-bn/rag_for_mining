from typing import List, Optional, Any
import uuid
import os
import vertexai
from app.common.constants import PROJECT_ID, REGION
from app.domain.interfaces.vector_store import VectorStoreInterface
from app.domain.models import Document as DomainDocument
from langchain.retrievers import MultiVectorRetriever
from langchain_core.stores import InMemoryStore
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document as LangchainDocument
from langchain_google_vertexai import VertexAIEmbeddings

class ChromaDBImpl(VectorStoreInterface):
    """
    Concrete implementation of the VectorStoreInterface using ChromaDB.
    """
    def __init__(self):
        vertexai.init(project=PROJECT_ID, location=REGION)
        
        embeddings = VertexAIEmbeddings(model_name="gemini-embedding-001", project=PROJECT_ID, location=REGION)
        
        # AWS Lambda only allows writing to /tmp
        is_lambda = os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is not None
        persist_dir = "/tmp/chroma_db" if is_lambda else "./chroma_db"
        
        self.vectorstore = Chroma(
            collection_name="mm_rag_cj_blog",
            embedding_function=embeddings,
            persist_directory=persist_dir
        )
        self.store = InMemoryStore()
        self.id_key = "doc_id"
        self.retriever = MultiVectorRetriever(
            vectorstore=self.vectorstore,
            docstore=self.store,
            id_key=self.id_key,
        )

    def get_retriever(self) -> Any:
        return self.retriever

    async def add_documents(self, documents: List[DomainDocument]) -> None:
        pass

    async def search(self, query: str, top_k: int) -> List[DomainDocument]:
        # Using LangChain retriever to search
        return self.retriever.invoke(query)[:top_k]

    async def search_multimodal(self, query: str, image_features: Optional[List[float]], top_k: int) -> List[DomainDocument]:
        pass
    
    def add_summaries_and_docs(self, doc_summaries: List[str], doc_contents: List[str], batch_size: int = 100):
        """
        Adds raw documents and their generated summaries into the VectorStore and InMemoryStore.
        """
        for i in range(0, len(doc_summaries), batch_size):
            batch_summaries = doc_summaries[i:i + batch_size]
            batch_contents = doc_contents[i:i + batch_size]
            doc_ids = [str(uuid.uuid4()) for _ in batch_contents]
            summary_docs = [
                LangchainDocument(page_content=s, metadata={self.id_key: doc_ids[j]})
                for j, s in enumerate(batch_summaries)
            ]
            self.retriever.vectorstore.add_documents(summary_docs)
            self.retriever.docstore.mset(list(zip(doc_ids, batch_contents)))

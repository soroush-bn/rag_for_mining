from app.domain.models import QueryRequest, QueryResponse
from app.domain.interfaces.vector_store import VectorStoreInterface
from app.domain.interfaces.multimodal_llm import MultimodalLLMInterface

class QAInteractor:
    """
    Use Case for executing the RAG Question & Answer workflow.
    """
    def __init__(
        self, 
        vector_store: VectorStoreInterface, 
        llm_service: MultimodalLLMInterface
    ):
        self.vector_store = vector_store
        self.llm_service = llm_service

    async def execute(self, request: QueryRequest) -> QueryResponse:
   
        retriever = self.vector_store.get_retriever()
        
        chain = self.llm_service.multi_modal_rag_chain(retriever)
        
        answer = chain.invoke(request.query_text)

        return QueryResponse(answer=answer, sources=[])

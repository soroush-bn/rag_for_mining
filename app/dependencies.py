import os
from dotenv import load_dotenv
from functools import lru_cache
from fastapi import Depends
from app.infrastructure.db.pinecone_db_impl import PineconeDBImpl
from app.infrastructure.services.multimodal_llm_impl import GeminiMultimodalLLMImpl
from app.use_cases.ingestion_interactor import IngestionInteractor
from app.use_cases.qa_interactor import QAInteractor
from app.domain.interfaces.multimodal_llm import MultimodalLLMInterface
from app.domain.interfaces.vector_store import VectorStoreInterface

load_dotenv()

@lru_cache() #singleton
def get_vector_store() -> VectorStoreInterface:
    return PineconeDBImpl()

@lru_cache()
def get_llm_service() -> MultimodalLLMInterface:
    return GeminiMultimodalLLMImpl()

def get_ingestion_interactor(
    vector_store: VectorStoreInterface = Depends(get_vector_store),
    llm_service: MultimodalLLMInterface = Depends(get_llm_service)
) -> IngestionInteractor:
    return IngestionInteractor(vector_store=vector_store, llm_service=llm_service)

def get_qa_interactor( 
    vector_store: VectorStoreInterface = Depends(get_vector_store),
    llm_service: MultimodalLLMInterface = Depends(get_llm_service)
) -> QAInteractor:
    return QAInteractor(vector_store=vector_store, llm_service=llm_service)

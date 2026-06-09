from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.domain.models import QueryRequest, QueryResponse
from app.use_cases.qa_interactor import QAInteractor
from app.use_cases.ingestion_interactor import IngestionInteractor
from app.dependencies import get_qa_interactor, get_ingestion_interactor

router = APIRouter(prefix="/api/v1/rag", tags=["Multimodal RAG"])

@router.post("/ask", response_model=QueryResponse)
async def ask_question(
    request: QueryRequest,
    qa_interactor: QAInteractor = Depends(get_qa_interactor)
):
    """
    Endpoint to ask a question (text + optional image URL) to the RAG system.
    """
    return await qa_interactor.execute(request)

@router.post("/ingest")
async def ingest_document(
    modality: str = Form(...),
    file: UploadFile = File(...),
    ingestion_interactor: IngestionInteractor = Depends(get_ingestion_interactor)
):
    """
    Endpoint to upload and ingest a document (Text, PDF, Image) into the RAG database.
    """
    file_bytes = await file.read()
    result = await ingestion_interactor.ingest_file(file.filename, file_bytes, modality)
    return result

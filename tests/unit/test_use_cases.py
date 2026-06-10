import pytest
from unittest.mock import MagicMock, AsyncMock
from app.use_cases.qa_interactor import QAInteractor
from app.domain.models import QueryRequest

@pytest.mark.asyncio
async def test_qa_interactor_execute_calls_dependencies():
    mock_vector_store = MagicMock()
    mock_llm_service = MagicMock()
    
    mock_retriever = MagicMock()
    mock_vector_store.get_retriever.return_value = mock_retriever
    
    mock_chain = MagicMock()
    mock_llm_service.multi_modal_rag_chain.return_value = mock_chain
    mock_chain.invoke.return_value = "Mocked Answer"

    interactor = QAInteractor(mock_vector_store, mock_llm_service)
    request = QueryRequest(query_text="What is safety?", top_k=5)
    
    response = await interactor.execute(request)
    
    assert response.answer == "Mocked Answer"
    mock_vector_store.get_retriever.assert_called_once()
    mock_llm_service.multi_modal_rag_chain.assert_called_once_with(mock_retriever)

# @pytest.mark.asyncio
# async def test_ingestion_interactor_processes_pdf(monkeypatch):
#     # Mock dependencies
#     mock_vector_store = MagicMock()
#     mock_llm_service = MagicMock()
    
#     # Mock LLM service methods
#     mock_llm_service.load_and_extract_text_from_pdf.return_value = ["Page 1 content"]
#     # Use AsyncMock for async methods
#     mock_llm_service.generate_text_summaries = AsyncMock(return_value=(["Summary 1"], []))
    
#     # Instantiate interactor
#     from app.use_cases.ingestion_interactor import IngestionInteractor
#     interactor = IngestionInteractor(mock_vector_store, mock_llm_service)
    
#     # Mock os.makedirs and os.remove to avoid file system interaction
#     monkeypatch.setattr("os.makedirs", lambda *args, **kwargs: None)
#     monkeypatch.setattr("os.remove", lambda *args, **kwargs: None)
#     # Mock 'open' to avoid writing real files
#     from unittest.mock import mock_open
#     monkeypatch.setattr("builtins.open", mock_open())

#     result = await interactor.ingest_file("test.pdf", b"content", "pdf")
    
#     assert result["status"] == "success"
#     assert "Ingested 1 pages" in result["message"]
    
#     mock_llm_service.load_and_extract_text_from_pdf.assert_called_once()
#     mock_llm_service.generate_text_summaries.assert_called_once()
#     mock_vector_store.add_summaries_and_docs.assert_called_once_with(
#         doc_summaries=["Summary 1"],
#         doc_contents=["Page 1 content"]
#     )

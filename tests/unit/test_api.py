# import pytest
# from fastapi.testclient import TestClient
# from unittest.mock import MagicMock
# from app.main import app
# from app.dependencies import get_qa_interactor, get_ingestion_interactor

# client = TestClient(app)

# # Override dependencies to use mocks during API tests
# @pytest.fixture(autouse=True)
# def mock_api_dependencies():
#     mock_qa = MagicMock()
#     mock_ingest = MagicMock()
#     app.dependency_overrides[get_qa_interactor] = lambda: mock_qa
#     app.dependency_overrides[get_ingestion_interactor] = lambda: mock_ingest
#     yield
#     app.dependency_overrides = {}

# def test_health_check():
#     response = client.get("/health")
#     assert response.status_code == 200
#     assert response.json() == {"status": "healthy"}

# def test_ask_endpoint_definition_ask():
#     response = client.post("/api/v1/rag/ask", json={})
#     assert response.status_code == 422 

# def test_ingest_endpoint_definition_ingest():
#     response = client.post('/api/v1/rag/ingest/',json={})
#     assert response.status_code==422

# def test_ingest_endpoint_accept_pdf():
#     """Test that the ingest endpoint correctly receives a PDF file and modality."""
#     file_content = b"fake pdf content"
#     files = {"file": ("test.pdf", file_content, "application/pdf")}
#     data = {"modality": "pdf"}
    
#     response = client.post("/api/v1/rag/ingest", files=files, data=data)
    
#     # With mocked dependencies, this should now be a 200
#     assert response.status_code == 200

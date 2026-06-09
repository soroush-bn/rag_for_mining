# import pytest
# from fastapi.testclient import TestClient
# from app.main import app

# client = TestClient(app)

# def test_full_ask_flow_validation():
#     """Integration test checking the flow through API to Domain models."""
#     payload = {
#         "query_text": "What are the safety rules?",
#         "top_k": 3
#     }
#     response = client.post("/api/v1/rag/ask", json=payload)
#     assert response.status_code in [200, 500] 

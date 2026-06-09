# import pytest
# import os
# from unittest.mock import MagicMock, patch

# # We patch the heavy dependencies before importing the class that uses them
# with patch("langchain_google_vertexai.VertexAIEmbeddings"), \
#      patch("langchain_community.vectorstores.Chroma"), \
#      patch("vertexai.init"):
#     from app.infrastructure.db.vector_db_impl import ChromaDBImpl

# def test_chroma_db_path_selection(monkeypatch):
#     # Mock the Chroma class inside the module
#     with patch("app.infrastructure.db.vector_db_impl.Chroma") as mock_chroma:
#         # Test local path
#         monkeypatch.delenv("AWS_LAMBDA_FUNCTION_NAME", raising=False)
#         db_local = ChromaDBImpl()
        
#         # Check that Chroma was called with the local path
#         args, kwargs = mock_chroma.call_args
#         assert kwargs["persist_directory"] == "./chroma_db"

#         # Test Lambda path
#         monkeypatch.setenv("AWS_LAMBDA_FUNCTION_NAME", "test-function")
#         db_lambda = ChromaDBImpl()
        
#         args, kwargs = mock_chroma.call_args
#         assert kwargs["persist_directory"] == "/tmp/chroma_db"

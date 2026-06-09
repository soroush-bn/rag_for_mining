import pytest
import os
from app.infrastructure.db.vector_db_impl import ChromaDBImpl

def test_chroma_db_path_selection(monkeypatch):
    # Test local path
    monkeypatch.delenv("AWS_LAMBDA_FUNCTION_NAME", raising=False)
    db_local = ChromaDBImpl()
    assert db_local.vectorstore._persist_directory == "./chroma_db"

    # Test Lambda path
    monkeypatch.setenv("AWS_LAMBDA_FUNCTION_NAME", "test-function")
    db_lambda = ChromaDBImpl()
    assert db_lambda.vectorstore._persist_directory == "/tmp/chroma_db"

import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from main import app

documents_list =[
    {"id": "testid1", "original_filename": "testfile1.pdf"},
    {"id": "testid2", "original_filename": "testfile2.pdf"},
]

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_db(mocker):
    mock = AsyncMock()
    mock.fetch_all_documents.return_value = documents_list
    mocker.patch("database.RedisDB.get_or_create", return_value=mock)
    return mock

@pytest.fixture
def mock_storage(mocker):
    mock = AsyncMock()
    mocker.patch("storage.FileSystemStorage.create", return_value=mock)
    return mock

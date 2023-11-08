import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_db(mocker):
    mock = AsyncMock()
    mocker.patch("database.RedisDB.get_or_create", return_value=mock)
    return mock

@pytest.fixture
def mock_storage(mocker):
    mock = AsyncMock()
    mocker.patch("storage.FileSystemStorage.create", return_value=mock)
    return mock

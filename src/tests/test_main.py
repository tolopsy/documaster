
from pathlib import Path
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

from .testutils import is_4xx, is_2xx

TEST_DATA_DIR = Path(__file__).resolve().parent / "data"
TEST_BAD_UPLOAD_DATA = TEST_DATA_DIR / "test_bad_upload.png"
TEST_GOOD_UPLOAD_DATA = TEST_DATA_DIR / "test_good_upload.pdf"


def test_post_upload_returns_4xx_for_unsupported_file_types(client: TestClient):
    with open(TEST_BAD_UPLOAD_DATA, "rb") as f:
        response = client.post("/upload", files={"files": f})

    assert is_4xx(response.status_code)

def test_post_upload_unsupported_file_not_stored(client: TestClient):
    with patch("storage.FileSystemStorage.store") as mock_storage:
        with open(TEST_BAD_UPLOAD_DATA, "rb") as f:
            _ = client.post("/upload", files={"files": f})
        
        mock_storage.assert_not_called()

def test_post_upload_unsupported_file_not_saved_to_db(client: TestClient):
    with patch("database.RedisDB.get_or_create") as mock_db:
        with open(TEST_BAD_UPLOAD_DATA, "rb") as f:
            _ = client.post("/upload", files={"files": f})
        
        mock_db.assert_not_called()

def test_post_upload_returns_2xx_for_supported_file_types(client: TestClient, mock_storage, mock_db):
    with open(TEST_GOOD_UPLOAD_DATA, "rb") as f:
        response = client.post("/upload", files={"files": f})

    assert is_2xx(response.status_code)

def test_post_upload_stores_supported_file_in_storage(
        client: TestClient,
        mock_storage: AsyncMock,
        mock_db: AsyncMock
    ):

    with open(TEST_GOOD_UPLOAD_DATA, "rb") as f:
        _ = client.post("/upload", files={"files": f})

    mock_storage.store.assert_called_once()

def test_post_upload_saves_document_in_db(
        client: TestClient,
        mock_storage: AsyncMock,
        mock_db: AsyncMock
    ):

    with open(TEST_GOOD_UPLOAD_DATA, "rb") as f:
        _ = client.post("/upload", files={"files": f})

    mock_db.save_document.assert_called_once()


def test_list_document(client: TestClient, mock_db: AsyncMock):
    response = client.get("/documents")
    mock_db.fetch_all_documents.assert_called_once()
    assert response.json() == mock_db.fetch_all_documents.return_value

# TODO: Split 'test_ask' into separate unit tests for each stage in the 'ask' endpoint
def test_ask(client: TestClient, mock_db: AsyncMock, mock_storage: AsyncMock):
    ...

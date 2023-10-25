from schemas.document import Document
from database import DB
from config import settings
    

async def fetch_documents_to_inquire(document_ids: list[str], db: DB) -> list[Document]:
    if document_ids:
        docs = await db.fetch_documents_by_ids(ids=document_ids)
    else:
        docs = await db.fetch_all_documents()
    
    return docs

def is_supported_file_type(filename: str | None) -> str | None:
    extension = filename.rsplit(".", maxsplit=1).pop() if "." in filename else None
    return extension.lower() in settings.SUPPORTED_FILE_TYPES

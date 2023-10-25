from schemas.document import Document
from database import DB

async def fetch_documents_to_inquire(document_ids: list[str], db: DB) -> list[Document]:
    if document_ids:
        docs = await db.fetch_documents_by_ids(ids=document_ids)
    else:
        docs = await db.fetch_all_documents()
    
    return docs

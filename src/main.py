from contextlib import asynccontextmanager
from secrets import token_hex

from fastapi import FastAPI, UploadFile, status, Depends
from fastapi.exceptions import HTTPException

from llm.vectorstore import get_vectorstore_retriever
from llm.conversation import create_openai_conversation_chain

from config import settings

from schemas.document import Document
from schemas.inquiry import Inquiry, InquiryResponse

from storage import FileSystemStorage, Storage
from database import RedisDB, DB, DocumentDoesNotExist
from dependencies import validate_supported_types


storage: Storage = FileSystemStorage.create(settings.UPLOAD_DIR)

async def get_db() -> DB:
    db = await RedisDB.get_or_create(settings.REDIS_URL)
    return db

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = await get_db()
    yield
    await db.close()


app = FastAPI(
    title="DocuMaster",
    summary="DocuMaster has a unique ability to answer questions or summarize documents",
    openapi_url="/api/v1/openapi.json",
    docs_url="/",
    lifespan=lifespan
)


@app.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    description=f"Upload Documents. Documents must be of supported types: {settings.SUPPORTED_FILE_TYPES}",
    response_model=list[Document]
)
async def upload(files: list[UploadFile] = Depends(validate_supported_types), db: DB = Depends(get_db)):
    docs = []

    for file in files:
        document = Document(id=token_hex(8), original_filename=file.filename)
        await storage.store(source_file=file, destination=document.name)
        await db.save_document(document)
        docs.append(document)
    
    return docs


@app.get("/documents", response_model=list[Document])
async def list_documents(db: DB = Depends(get_db)) -> None:
    docs = await db.fetch_all_documents()
    return docs


@app.post("/ask", response_model=InquiryResponse)
async def ask(inquiry: Inquiry, db: DB = Depends(get_db)):
    document_ids = inquiry.document_ids
    if document_ids:
        try:
            docs = await db.fetch_documents_by_ids(ids=document_ids)
        except DocumentDoesNotExist as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid document id: {e.doc_id}"
            )
    else:
        docs = await db.fetch_all_documents()

    if not docs:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No document"
        )

    vectorstore_retriever = get_vectorstore_retriever(
        storage=storage,
        folder_path=str(settings.VECTORSTORE_DIR),
        docs=docs
    )

    # ask question
    conversation_chain = create_openai_conversation_chain(retriever=vectorstore_retriever)
    response = conversation_chain({"question": inquiry.question})

    return response

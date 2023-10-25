from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol
from langchain.vectorstores.faiss import FAISS

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders.base import BaseLoader
from schemas.document import Document as DocumentSchema, UnsupportedDocumentTypeError
from .embeddings import get_openai_embeddings


class FileLocator(Protocol):
    def get_file_location(file_name: str) -> str:
        ...


@dataclass
class FAISSWrapper:
    """Custom wrapper for faiss vectorstore"""
    faiss: FAISS

    def __add__(self, other: FAISSWrapper):
        if not isinstance(other, FAISSWrapper):
            raise TypeError("Unsupported operand type for +")

        self.faiss.merge_from(other.faiss)
        return self
    
    def as_retriever(self, **kwargs):
        return self.faiss.as_retriever(**kwargs)


def get_document_loader(*, doc_extension: str, doc_location: str) -> BaseLoader:
    if doc_extension.lower() == "pdf":
        return PyPDFLoader(doc_location)
    
    else:
        raise UnsupportedDocumentTypeError(
            doc_type=doc_extension,
            message=f"Document of type: {doc_extension} cannot be loaded."
        )


def create_document_chunks(loader: BaseLoader) -> list(Document):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
    return loader.load_and_split(text_splitter=text_splitter)


def get_vectorstore(*, folder_path: str, doc: DocumentSchema, doc_location: str):
    embeddings = get_openai_embeddings()

    try:
        vectorstore = FAISS.load_local(
            folder_path=folder_path,
            embeddings=embeddings,
            index_name=doc.id
        )
    except Exception:
        loader = get_document_loader(doc_extension=doc.extension, doc_location=doc_location)
        vectorstore = FAISS.from_documents(
            documents=create_document_chunks(loader),
            embedding=embeddings
        )
        vectorstore.save_local(folder_path=folder_path, index_name=doc.id)
    
    return FAISSWrapper(faiss=vectorstore)


def get_vectorstore_retriever(*, storage: FileLocator, folder_path: str, docs: DocumentSchema):
    root_doc = docs[0]
    root_vectorstore = get_vectorstore(
        folder_path=folder_path,
        doc=root_doc,
        doc_location=storage.get_file_location(root_doc.name)
    )

    for doc in docs[1:]:
        vectorstore = get_vectorstore(
            folder_path=folder_path,
            doc=doc,
            doc_location=storage.get_file_location(doc.name)
        )

        root_vectorstore += vectorstore
    
    return root_vectorstore.as_retriever()

from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
import redis.asyncio as redis
from redis.asyncio import Redis
from redis.exceptions import ConnectionError as RedisConnectionError
from schemas.document import Document

class DocumentDoesNotExist(Exception):
    def __init__(self, doc_id: str, message: str):
        """Custom error raised when document with the given id does not exist in database"""
        self.doc_id = doc_id
        self.message = message
        super().__init__(message)

class DatabaseConnectionError(Exception):
    """Error raised when a connection to the database cannot be established."""


class DB(ABC):
    """Wrapper around database to hide implementation details"""
    
    @abstractmethod
    def fetch_documents_by_ids(self, ids: list[str]) -> list[Document]:
        ...

    @abstractmethod
    def fetch_all_documents(self) -> list[Document]:
        ...
    
    @abstractmethod
    def save_document(self, document: Document):
        ...
    
    @abstractmethod
    async def close(self):
        """Close connection to the database"""
        ...


@dataclass
class RedisDB(DB):
    """A Singleton Redis Database Wrapper """
    client: Redis
    _instance: RedisDB | None = None

    @classmethod
    async def create(cls, url: str) -> RedisDB:
        client = await redis.from_url(url)
        try:
            await client.ping()
        except RedisConnectionError as e:
            raise DatabaseConnectionError(f"Redis failed to connect: {e}")
        
        return cls(client=client)

    @classmethod
    async def get_or_create(cls, url: str) -> RedisDB:
        """Returns a Singleton RedisDB to prevent multiple client connections per request."""
        if cls._instance == None:
            cls._instance = await cls.create(url)

        return cls._instance

    def _add_document_prefix(self, doc_id: str):
        return f"doc:{doc_id}"
    
    async def fetch_documents_by_ids(self, ids: list[str]) -> list[Document]:
        docs = []
        for doc_id in ids:
            key = self._add_document_prefix(doc_id)
            value = await self.client.get(key)
            if not value:
                raise DocumentDoesNotExist(doc_id=doc_id, message="invalid document id: {doc_id}")
            doc = Document.model_validate_json(value.decode("utf-8"))
            docs.append(doc)
        
        return docs

    async def fetch_all_documents(self) -> list[Document]:
        keys_wildcard = self._add_document_prefix("*")

        keys = await self.client.keys(keys_wildcard)

        docs = []
        for key in keys:
            value = await self.client.get(key)
            if not value:
                continue

            doc = Document.model_validate_json(value.decode("utf-8"))
            docs.append(doc)

        return docs

    async def save_document(self, document: Document):
        key = self._add_document_prefix(document.id)
        await self.client.set(name=key, value=document.model_dump_json())
    
    async def close(self):
        await self.client.aclose()

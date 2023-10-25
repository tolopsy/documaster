from abc import ABC, abstractmethod
from typing import Protocol

DEFAULT_CHUNK_SIZE = 10 * 1024 * 1024   # 10MB


class FileReader(Protocol):
    async def read(self, size: int) -> bytes:
        ...


class Storage(ABC):
    @abstractmethod
    def get_file_location(self, file_name: str) -> str:
        """Get file location from storage"""
    
    @abstractmethod
    async def store(self, source_file: FileReader, destination: str) -> None:
        """Save file to storage"""

from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
import aiofiles
from .base import Storage, FileReader, DEFAULT_CHUNK_SIZE


@dataclass
class FileSystemStorage(Storage):
    root: str

    @classmethod
    def create(cls, url: Path) -> FileSystemStorage:
        """Setup FileSystem Storage. The url argument represents the root folder"""

        url.mkdir(exist_ok=True, parents=True)
        return cls(root=str(url))
    
    def get_file_location(self, file_name: str) -> str:
        return os.path.join(self.root, file_name)

    async def store(
            self,
            source_file: FileReader,
            destination: str,
            chunk_size: int = DEFAULT_CHUNK_SIZE
        ) -> None:

        location = self.get_file_location(destination)
        
        # read data from source file in chunk and write to destination
        async with aiofiles.open(location, "wb") as file:
            while chunk := await source_file.read(chunk_size):
                await file.write(chunk)

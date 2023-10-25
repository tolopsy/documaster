from pydantic import BaseModel, field_validator
from enum import Enum


class NoFileExtensionError(Exception):
    """Custom error raised when document has no file extension"""
    pass

class UnsupportedDocumentTypeError(Exception):
    def __init__(self, doc_type: str, message: str):
        """Custom error raised when document is not supported"""

        self.doc_type = doc_type
        self.message = message
        super().__init__(message)


class Document(BaseModel):
    """Document"""
    id: str
    original_filename: str
    
    @field_validator("original_filename")
    @classmethod
    def original_filename_has_extension(cls, value: str):
        if len(value.rsplit(".", maxsplit=1)) != 2:
            raise NoFileExtensionError(f"Filename must have an extension: {value}")
        return value
    
    @property
    def extension(self) -> str:
        return self.original_filename.rsplit(".").pop()
    
    @property
    def name(self) -> str:
        return f"{self.id}.{self.extension}"

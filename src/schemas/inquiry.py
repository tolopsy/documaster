from pydantic import BaseModel, Field


class Inquiry(BaseModel):
    document_ids: list[str] = Field(default_factory=list)
    question: str


class InquiryResponse(BaseModel):
    question: str
    answer: str
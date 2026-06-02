
from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict

from db.models import Status

class DocumentRequest(BaseModel):
    name: str
    content: str

class DocumentChunkRequest(BaseModel):
    document_id: uuid.UUID
    chunk: str
    chunk_index: int
    embedding: list[float]

class DocumentResponse(BaseModel):
    id: uuid.UUID
    name: str
    status: Status
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DocumentChunkResponse(BaseModel):
    id: uuid.UUID
    chunk: str
    chunk_index: int
    created_at: datetime
    document_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

class SearchRequest(BaseModel):
    query: str
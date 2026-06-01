
import uuid
from pydantic import BaseModel

class DocumentRequest(BaseModel):
    name: str
    content: str

class DocumentChunkRequest(BaseModel):
    document_id: uuid.UUID
    chunk: str
    chunk_index: int
    embedding: list[float]

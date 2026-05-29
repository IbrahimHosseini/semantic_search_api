
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

import uuid

from .base import Base
from enum import Enum


class Status(str, Enum):
    pending="pending"
    processing="processing"
    completed="completed"
    failed="failed"

class Document(Base):
    __tablename__ = "document"
    name: Mapped[str] = mapped_column(String(255), default="")
    file_path: Mapped[str] = mapped_column(String(255), default="")
    status: Mapped[Status] = mapped_column(SAEnum(Status), default=Status.pending)

    document_chunks: Mapped[list["DocumentChunk"]] = relationship(
        "DocumentChunk", back_populates="document"
    )

class DocumentChunk(Base):
    __tablename__ = "document_chunk"
    chunk: Mapped[str] = mapped_column(Text, default="")
    chunk_index: Mapped[int] = mapped_column(index=True)
    embedding: Mapped[list[float]] = mapped_column(Vector(1536))

    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("document.id"))

    document: Mapped["Document"] = relationship(
        "Document", back_populates="document_chunks"
    )
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Document, DocumentChunk
from app.schemas import DocumentRequest, DocumentChunkRequest

async def create_document(session: AsyncSession, document: DocumentRequest) -> Document | None:

    new_document = Document(
        name = document.name,
        file_path = document.file_path
    )

    session.add(new_document)
    await session.commit()
    await session.refresh(new_document)

    return new_document


async def create_document_checks(session: AsyncSession, document_chunks: list[DocumentChunkRequest]) -> list[DocumentChunk] | None:

    new_document_chunks = []

    for dc in document_chunks:
        new_dc = DocumentChunk(
            chunk=dc.chunk,
            chunk_index=dc.chunk_index,
            embedding=dc.embedding,
            document_id=dc.document_id
        )

        new_document_chunks.append(new_dc)

    session.add_all(new_document_chunks)
    await session.commit()
    for chunk in new_document_chunks:
        await session.refresh(chunk)

    return new_document_chunks

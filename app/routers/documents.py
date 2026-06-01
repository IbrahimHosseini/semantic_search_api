import uuid
from fastapi import APIRouter, Depends, status, HTTPException
from db.models import Document,  DocumentChunk
from db.session import get_db
from services.embedding import get_embedding, chunk_text
from db.repositories import document_repository
from app.schemas import DocumentChunkRequest, DocumentRequest

router = APIRouter()

@router.post("/documents/", status_code=status.HTTP_201_CREATED)
async def upload_text(document_request: DocumentRequest, session=Depends(get_db)):

    new_create_document = await document_repository.create_document(
        session=session,
        document=document_request
    )

    chunks = await chunk_text(text=document_request.name)

    document_chunks: list[DocumentChunkRequest] = []
    document_id = uuid.uuid4

    for chunk in chunks:
        embedding = await get_embedding(chunk)

        new_document_chunk = DocumentChunkRequest(
            document_id=document_id,
            chunk=chunk,
            chunk_index=0,
            embedding=embedding
        )
        document_chunks.append(new_document_chunk)

    document_repository.create_document_checks(session=session, document_chunks=document_chunks)

@router.get("/documents/", response_model=list[Document])
async def get_document():
    get_embedding()

@router.post("/documents/search", response_model=list[DocumentChunk])
async def search(query: str):
    try:
        await chunk_text(text=query)
    except Exception:
        raise HTTPException(status_code=404, detail="Not found")

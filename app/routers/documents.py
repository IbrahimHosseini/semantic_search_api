import uuid
from fastapi import APIRouter, Depends, status, HTTPException
from db.session import get_db
from services.embedding import get_embedding, chunk_text
from db.repositories import document_repository
from app.schemas import DocumentChunkRequest, DocumentRequest, DocumentResponse, DocumentChunkResponse, SearchRequest

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/", response_model=DocumentResponse,status_code=status.HTTP_201_CREATED)
async def upload_text(document_request: DocumentRequest, session=Depends(get_db)):

    new_create_document = await document_repository.create_document(
        session=session,
        document=document_request
    )

    chunks = chunk_text(text=document_request.content)

    document_chunks: list[DocumentChunkRequest] = []

    for index,chunk in enumerate(chunks):
        embedding = await get_embedding(chunk)

        new_document_chunk = DocumentChunkRequest(
            document_id=new_create_document.id,
            chunk=chunk,
            chunk_index=index,
            embedding=embedding
        )
        document_chunks.append(new_document_chunk)

    await document_repository.create_document_checks(session=session, document_chunks=document_chunks)

    return new_create_document

@router.get("/", response_model=list[DocumentResponse])
async def get_document(session = Depends(get_db)):
    documents = await document_repository.get_documents(session=session)
    return documents

@router.post("/search", response_model=list[DocumentChunkResponse])
async def search(request: SearchRequest, session = Depends(get_db)):
    try:
        embedding_list = await get_embedding(text=request.query)

        document_chunks = await document_repository.search_similar_chunks(
                session=session,
                embedding=embedding_list
            )
        return document_chunks

    except Exception:
        raise HTTPException(status_code=404, detail="Not found")

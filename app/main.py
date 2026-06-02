from fastapi import FastAPI
from .routers import documents


app = FastAPI(
    title= "Semantic search API",
    description="API for semantic search",
    version="0.1.0",
)

app.include_router(documents.router)

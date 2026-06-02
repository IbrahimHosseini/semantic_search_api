# Semantic Search API

[![CI](https://github.com/IbrahimHosseini/semantic_search_api/actions/workflows/ci.yml/badge.svg)](https://github.com/IbrahimHosseini/semantic_search_api/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Coverage](https://img.shields.io/badge/coverage-%E2%89%A580%25-brightgreen.svg)](https://github.com/IbrahimHosseini/semantic_search_api)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

FastAPI service for semantic document search using OpenAI embeddings and pgvector cosine similarity.

## Stack

- **FastAPI** — async REST API
- **PostgreSQL + pgvector** — vector storage and cosine similarity search
- **SQLAlchemy 2.0** — async ORM
- **OpenAI** `text-embedding-3-small` — 1536-dim embeddings
- **Alembic** — async database migrations

## Project Structure

```text
semantic_search_api/
├── app/
│   ├── main.py              # FastAPI app setup
│   ├── schemas.py           # Pydantic request/response models
│   └── routers/
│       └── documents.py     # Document and search endpoints
├── db/
│   ├── base.py              # SQLAlchemy declarative base
│   ├── models.py            # Document and DocumentChunk models
│   ├── session.py           # Async engine and session factory
│   └── repositories/
│       └── document_repository.py  # DB operations
├── services/
│   └── embedding.py         # OpenAI embedding client + text chunker
├── alembic/                 # Migration scripts
├── config.py                # Pydantic settings (env vars)
└── requirements.txt
```

## Setup

### Prerequisites

- Python 3.13+
- PostgreSQL with pgvector extension enabled
- OpenAI API key

### Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Environment

Create a `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
OPENAI_API_KEY=sk-...
```

### Database

Enable pgvector in PostgreSQL:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Run migrations:

```bash
alembic upgrade head
```

### Run

```bash
uvicorn app.main:app --reload
```

API available at `http://localhost:8000`. Docs at `http://localhost:8000/docs`.

## API

### Upload Document

`POST /documents/`

Stores a document, chunks it (500 chars, 50-char overlap), and generates embeddings for each chunk.

**Request:**

```json
{
  "name": "my-doc",
  "content": "Full document text..."
}
```

**Response:**

```json
{
  "id": "uuid",
  "name": "my-doc",
  "status": "pending",
  "created_at": "2026-06-03T00:00:00"
}
```

### List Documents

`GET /documents/`

Returns all uploaded documents.

### Semantic Search

`POST /documents/search`

Embeds the query and returns the top 5 most similar chunks via cosine distance.

**Request:**

```json
{
  "query": "your search query"
}
```

**Response:**

```json
[
  {
    "id": "uuid",
    "chunk": "matching text chunk...",
    "chunk_index": 2,
    "document_id": "uuid",
    "created_at": "2026-06-03T00:00:00"
  }
]
```

## Data Models

### Document

| Field      | Type     | Description                                    |
|------------|----------|------------------------------------------------|
| id         | UUID     | Primary key                                    |
| name       | string   | Document name                                  |
| status     | enum     | `pending`, `processing`, `completed`, `failed` |
| created_at | datetime | Auto-set on creation                           |

### DocumentChunk

| Field       | Type         | Description              |
|-------------|--------------|--------------------------|
| id          | UUID         | Primary key              |
| document_id | UUID (FK)    | Parent document          |
| chunk       | text         | Text chunk content       |
| chunk_index | int          | Position within document |
| embedding   | vector(1536) | OpenAI embedding         |
| created_at  | datetime     | Auto-set on creation     |

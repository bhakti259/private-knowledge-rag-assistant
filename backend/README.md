# Backend (FastAPI)

This module exposes the HTTP API for chat and ingestion.

## Responsibilities

- Route incoming requests (`app/api/routes`)
- Validate payloads (`app/schemas`)
- Orchestrate services (`app/services`)
- Read environment configuration (`app/core/config.py`)

## Entry Point

- `app/main.py` builds and configures the FastAPI application.

## Running the server

Run **from the `backend/` directory**:

```bash
# Option 1 — module path (recommended)
uvicorn app.main:app --reload

# Option 2 — convenience launcher at backend/run.py
# Watches backend/, ingestion/, rag_pipeline/, and vector_db/
python run.py

# Option 3 — compatibility shim
uvicorn main:app --reload
```

`backend/main.py` exists as a compatibility entrypoint so older commands still work.

> Note: plain `uvicorn ... --reload` started from `backend/` watches only the
> `backend/` folder. If you edit sibling modules like `vector_db/` or
> `rag_pipeline/`, do a full restart or use `python run.py`.

## Install dependencies

```bash
pip install -r requirements.txt
```

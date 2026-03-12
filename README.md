# Private AI Knowledge Agent — MVP Skeleton

This repository is a **modular scaffold** for a Private AI Knowledge Agent using:

- **FastAPI** backend API
- **React (Vite + TypeScript)** frontend
- **LangGraph** for agent orchestration
- **RAG + Chroma** for retrieval
- **Ollama** for local LLM inference

Each module is intentionally separated so you can implement and test parts independently.

## Repository Layout

```text
agents/        -> LangGraph state, nodes, and graph wiring
backend/       -> FastAPI app, routes, schemas, and service layer
frontend/      -> React UI for chat + ingestion controls
ingestion/     -> Document loading/chunking/indexing pipeline
rag_pipeline/  -> Retrieval + prompt composition logic
vector_db/     -> Chroma client wrapper and persistence folder
```

## Suggested Implementation Order

1. Implement `vector_db/chroma_client.py` with real Chroma operations.
2. Implement `ingestion/pipeline.py` to upsert chunked docs.
3. Implement `rag_pipeline/retriever.py` + `rag_pipeline/chain.py`.
4. Replace placeholders in `backend/app/services/*.py`.
5. Wire actual LangGraph flow in `agents/graph.py`.
6. Connect frontend forms to backend endpoints.

## Local Run Targets (after implementation)

- Backend: `uvicorn app.main:app --reload` (from `backend/`)
- Frontend: `npm run dev` (from `frontend/`)

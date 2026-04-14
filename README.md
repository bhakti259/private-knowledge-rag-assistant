# Private AI Knowledge Agent

A private, self-hosted AI knowledge agent that lets you **upload PDFs**, **embed them into a local vector store**, and **ask natural-language questions** — powered by OpenAI embeddings, ChromaDB retrieval, and GPT-4o-mini answer generation. Built with a FastAPI backend and a React frontend.

## Stack

| Layer | Technology |
| --- | --- |
| Backend API | FastAPI + Uvicorn |
| PDF ingestion | PyPDF2 |
| Embeddings | OpenAI `text-embedding-3-small` |
| Answer Generation | OpenAI `gpt-4o-mini` via LangChain |
| Vector store | ChromaDB (local, persistent) |
| Agent orchestration | LangGraph (scaffold) |
| Local LLM | Ollama (scaffold) |
| Frontend | React + Vite + TypeScript + Axios |

## Repository Layout

```text
agents/          LangGraph state, nodes, and graph wiring (scaffold)
backend/         FastAPI app — routes, schemas, services, config
  app/
    api/routes/  upload_pdf, ask_question, chat, ingest, health
    core/        config.py (pydantic-settings, loads repo-root .env)
    services/    agent_service, rag_service, ollama_client
  main.py        compatibility entrypoint (supports `uvicorn main:app`)
  run.py         convenience dev launcher (watches all source dirs)
frontend/        React UI — IngestPanel (PDF upload) + ChatPanel (Q&A)
ingestion/       PDF loader (PyPDF2) + text chunker
rag_pipeline/    Retriever, prompt builder, answer generation (GPT-4o-mini)
vector_db/       ChromaDB client + store_embeddings helper
```

## Quick Start

### 1. Install Python dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure environment

```bash
# From repo root
copy .env.example .env
# Edit .env and set OPENAI_API_KEY=sk-...
```

### 3. Run the backend

```bash
cd backend
python run.py          # recommended — watches all source dirs
# or
uvicorn main:app --reload
```

API docs available at: `http://127.0.0.1:8000/docs`

### 4. Run the frontend

```bash
cd frontend
npm install
npm start        # alias for `npm run dev`, starts at http://localhost:5173
```

The frontend wires directly to the backend at `http://127.0.0.1:8000`:

- **IngestPanel** — file picker + `POST /upload_pdf`, displays chunks stored
- **ChatPanel** — ask questions via `POST /ask_question`, displays generated answers with collapsible source references

## Architecture Flow

### Upload Flow

```
User selects PDF
     |
IngestPanel (React)
     |  POST /upload_pdf (multipart)
     v
upload.py ─── validate (name, extension, MIME)
     |
     ├──> _write_upload_to_disk()  ──>  backend/uploads/
     |
     ├──> loaders.py:extract_text_from_pdf()
     |         └──> PyPDF2  ──>  raw text string
     |
     ├──> chunking.py:chunk_text(600 chars, 80 overlap)
     |         └──> list of text chunks
     |
     └──> chroma_client.py:store_embeddings()
               ├──> OpenAI API (text-embedding-3-small)  ──>  1536-dim vectors
               └──> ChromaDB.add_texts()  ──>  persisted to disk

Response: { file_path, chunks_stored }
```

### Query Flow

```
User types question + Enter
     |
ChatPanel (React)
     |  POST /ask_question { query, top_k: 4 }
     v
ask.py ─── validate query
     |
     ├──> retriever.py:retrieve_answer()
     |         ├──> OpenAI API  ──>  embed query into vector
     |         └──> ChromaDB.similarity_search()  ──>  top 4 chunks + scores
     |
     └──> chain.py:generate_answer()
               ├──> build_rag_prompt()  ──>  format context + question
               └──> ChatOpenAI (gpt-4o-mini)  ──>  synthesized answer

Response: { query, answer, results: [chunks with scores] }
     |
ChatPanel renders:
     ├──> AI bubble with generated answer
     └──> Collapsible "Sources (3)" with chunk previews + scores
```

## Key Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Health check |
| `POST` | `/upload_pdf` | Upload a PDF → extracts text → chunks → embeds → stores in Chroma |
| `POST` | `/ask_question` | Ask a natural-language question — returns a generated answer + source chunks |
| `POST` | `/chat` | LangGraph agent chat (scaffold) |

## Environment Variables

See `.env.example` for the full list. Required for embedding:

```text
OPENAI_API_KEY=sk-...
```

## Notes

- The `.env` file must live at the **repo root** (next to `backend/`). The app always loads it from there regardless of where you start the server.
- `python run.py` from `backend/` is the recommended way to start locally — it wires hot-reload across `backend/`, `ingestion/`, `rag_pipeline/`, and `vector_db/`.
- LangGraph agent nodes and the Ollama chat route are scaffold-only and not yet fully wired.
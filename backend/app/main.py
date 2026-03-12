"""Application entrypoint.

This module wires middleware, routers, and high-level app settings.
"""

from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure repository root is importable when running from `backend/`.
# This lets sibling modules like `rag_pipeline/` and `vector_db/` resolve.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.api.routes import ask, chat, health, ingest, upload
from app.core.config import settings

# NOTE: API keys must never be hardcoded here — use the .env file instead.
# See .env.example for the full list of required environment variables.



def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(
        title="Private AI Knowledge Agent API",
        version="0.1.0",
        description="Backend API for chat, ingestion, and agent orchestration.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix="/health", tags=["health"])
    app.include_router(chat.router, prefix="/chat", tags=["chat"])
    app.include_router(ingest.router, prefix="/ingest", tags=["ingestion"])
    # PDF upload + ingestion pipeline
    app.include_router(upload.router, tags=["ingestion"])
    # Retrieval-only Q&A endpoint backed by Chroma
    app.include_router(ask.router, tags=["retrieval"])
    return app


app = create_app()

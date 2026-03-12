"""Ingestion endpoint module.

Receives document payloads and triggers ingestion workflows.
"""

from fastapi import APIRouter

from app.schemas.ingest import IngestRequest, IngestResponse

router = APIRouter()


@router.post("/", response_model=IngestResponse, summary="Queue documents for ingestion")
async def ingest(payload: IngestRequest) -> IngestResponse:
    """Accept document payloads and return queue/processing status.

    TODO:
        Wire this to `ingestion.pipeline.run_ingestion(...)`.
    """
    return IngestResponse(status="queued", documents_received=len(payload.documents))

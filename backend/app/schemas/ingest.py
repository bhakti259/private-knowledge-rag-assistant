"""Ingestion-related request/response models."""

from typing import Any

from pydantic import BaseModel, Field


class IngestDocument(BaseModel):
    """Single document input for the ingestion endpoint."""

    id: str
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class IngestRequest(BaseModel):
    """Batch payload for document ingestion."""

    documents: list[IngestDocument]


class IngestResponse(BaseModel):
    """Acknowledgement payload for ingestion request handling."""

    status: str
    documents_received: int

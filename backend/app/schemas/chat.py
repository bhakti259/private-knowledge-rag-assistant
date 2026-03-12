"""Chat-related request/response models.

These schemas define API contracts independent from service internals.
"""

from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Client payload for a chat turn."""

    message: str = Field(..., description="User query text")
    session_id: str | None = Field(default=None, description="Optional conversation/session ID")


class SourceChunk(BaseModel):
    """Minimal source metadata returned with responses."""

    id: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    """Response payload containing answer text and optional evidence."""

    answer: str
    sources: list[SourceChunk] = Field(default_factory=list)

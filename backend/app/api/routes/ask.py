"""/ask_question endpoint module.

Takes a plain-language query, runs similarity search against Chroma,
and returns the most relevant PDF chunks as structured JSON.

This endpoint is intentionally retrieval-only (no LLM generation) so it
can be used as a fast, inspectable first step before feeding results to
an LLM in the chat endpoint.
"""

import asyncio
from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from rag_pipeline.retriever import retrieve_answer
from rag_pipeline.chain import generate_answer

router = APIRouter()


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------

class AskRequest(BaseModel):
    """Payload sent by the client to /ask_question."""

    query: str = Field(..., description="Natural-language question to search for.")
    top_k: int = Field(default=4, ge=1, le=20, description="Number of chunks to return.")


class RetrievedChunk(BaseModel):
    """A single matched chunk returned by the retriever."""

    text: str = Field(..., description="Raw text content of the chunk.")
    source: str = Field(..., description="File the chunk was ingested from.")
    chunk_index: int = Field(..., description="Position of this chunk within its source file.")
    score: float = Field(..., description="Relevance score in [0, 1]; higher is more relevant.")
    metadata: dict[str, Any] = Field(default_factory=dict, description="All Chroma metadata fields.")


class AskResponse(BaseModel):
    """Retrieval result returned to the client."""

    query: str
    answer: str = Field(..., description="Generated natural-language answer.")
    results: list[RetrievedChunk]


# ---------------------------------------------------------------------------
# Endpoint
# ---------------------------------------------------------------------------

@router.post(
    "/ask_question",
    response_model=AskResponse,
    summary="Ask a question, retrieve relevant PDF chunks",
)
async def ask_question(payload: AskRequest) -> AskResponse:
    """Search Chroma for PDF chunks that best match the user's query.

    The endpoint:
      1. Validates the query is non-empty.
      2. Runs async-safe similarity search against the Chroma vector store.
      3. Returns an ordered list of matching chunks with scores and source info.
    """

    # Step 1: Reject blank queries before hitting any downstream service.
    if not payload.query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query must not be empty.",
        )

    # Step 2: Run the retriever in a thread pool so the async event loop is
    #         not blocked by synchronous LangChain / Chroma operations.
    try:
        raw_results: list[dict[str, Any]] = await asyncio.to_thread(
            retrieve_answer,
            payload.query,
            payload.top_k,
        )
    except EnvironmentError as exc:
        # Missing OPENAI_API_KEY — surface as 500 so the operator can fix config.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Retrieval failed: {exc}",
        ) from exc

    # Step 3: Map raw dicts returned by retrieve_answer into typed response models.
    chunks = [
        RetrievedChunk(
            text=item["text"],
            source=item["source"],
            chunk_index=item["chunk_index"],
            score=item["score"],
            metadata=item.get("metadata", {}),
        )
        for item in raw_results
    ]

    # Step 4: Generate a synthesized answer from the retrieved chunks.
    try:
        answer = await asyncio.to_thread(
            generate_answer,
            payload.query,
            raw_results,
        )
    except EnvironmentError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Answer generation failed: {exc}",
        ) from exc

    # Step 5: Return the structured response with the generated answer.
    return AskResponse(query=payload.query, answer=answer, results=chunks)

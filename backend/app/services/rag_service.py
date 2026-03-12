"""RAG service abstraction.

This service will own retrieval strategy and context shaping for prompts.
"""

from typing import Any


class RagService:
    """Coordinates retrieval calls and output normalization."""

    def retrieve(self, query: str, top_k: int = 4) -> list[dict[str, Any]]:
        """Fetch top-k context chunks for a given query.

        TODO:
            Wire this to `rag_pipeline.retriever.retrieve_chunks`.
        """
        _ = (query, top_k)
        return []

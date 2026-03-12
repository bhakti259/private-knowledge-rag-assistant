"""Retriever abstraction.

Focuses on similarity lookup and normalization of retrieval results.
"""

from typing import Any

from vector_db.chroma_client import ChromaVectorStore


def retrieve_chunks(query: str, top_k: int = 4) -> list[dict[str, Any]]:
    """Retrieve context chunks from Chroma for a user query."""
    vector_store = ChromaVectorStore()
    return vector_store.similarity_search(query=query, top_k=top_k)

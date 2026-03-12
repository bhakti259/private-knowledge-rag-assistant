"""Retriever abstraction.

Focuses on similarity lookup and normalization of retrieval results.
Exposes two callables:
  - `retrieve_answer(query)`  — high-level, returns structured results.
  - `retrieve_chunks(query)`  — thin wrapper kept for backward compatibility.
"""

from importlib import import_module
from typing import Any


def _get_settings():
    """Load application settings from either supported import path."""
    for module_name in ("app.core.config", "backend.app.core.config"):
        try:
            return import_module(module_name).settings
        except ModuleNotFoundError:
            continue
    raise ModuleNotFoundError("Could not import application settings.")


settings = _get_settings()


def retrieve_answer(
    query: str,
    top_k: int = 4,
    collection_name: str | None = None,
    persist_dir: str | None = None,
) -> list[dict[str, Any]]:
    """Search Chroma for the most relevant PDF chunks matching a user query.

    Args:
        query:           Natural-language question from the user.
        top_k:           How many top-matching chunks to return.
        collection_name: Chroma collection to search (falls back to env/default).
        persist_dir:     Chroma persistence directory (falls back to env/default).

    Returns:
        List of dicts, each with ``text``, ``source``, ``chunk_index``,
        and ``score`` keys, ordered from most to least relevant.
    """
    # Step 1: Resolve config from arguments or environment variables.
    resolved_collection = collection_name or settings.chroma_collection
    resolved_persist_dir = persist_dir or settings.chroma_persist_dir
    openai_api_key = settings.openai_api_key

    # Step 2: Guard against a missing API key with an actionable error.
    if not openai_api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY is not set. Add it to your .env file."
        )

    # Step 3: Guard against an empty query — nothing meaningful to search.
    if not query.strip():
        return []

    # Step 4: Import LangChain dependencies with a clear install hint on failure.
    try:
        from langchain_chroma import Chroma
        from langchain_openai import OpenAIEmbeddings
    except ImportError as exc:
        raise ImportError(
            "langchain-chroma and langchain-openai are required. "
            "Install them with: pip install langchain-chroma langchain-openai"
        ) from exc

    # Step 5: Build the same embedding model used at ingestion time so that
    #         query vectors are comparable to the stored document vectors.
    embedding_model = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=openai_api_key,
    )

    # Step 6: Connect to the persistent Chroma collection (read-only here).
    vector_store = Chroma(
        collection_name=resolved_collection,
        embedding_function=embedding_model,
        persist_directory=resolved_persist_dir,
    )

    # Step 7: Run similarity search and get back (Document, score) pairs.
    #         `similarity_search_with_relevance_scores` returns float scores
    #         in [0, 1] where higher means more relevant.
    results_with_scores = vector_store.similarity_search_with_relevance_scores(
        query=query,
        k=top_k,
    )

    # Step 8: Normalize results into a plain dict structure so callers don't
    #         depend on LangChain's Document type directly.
    normalized: list[dict[str, Any]] = []
    for document, score in results_with_scores:
        normalized.append({
            "text": document.page_content,
            "source": document.metadata.get("source", "unknown"),
            "chunk_index": document.metadata.get("chunk_index", -1),
            "score": round(score, 4),
            "metadata": document.metadata,
        })

    # Step 9: Sort by descending relevance score before returning.
    normalized.sort(key=lambda chunk: chunk["score"], reverse=True)

    return normalized


def retrieve_chunks(query: str, top_k: int = 4) -> list[dict[str, Any]]:
    """Thin wrapper around `retrieve_answer` kept for backward compatibility."""
    return retrieve_answer(query=query, top_k=top_k)

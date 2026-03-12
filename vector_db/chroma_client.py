"""Chroma wrapper.

This module is the only layer that should know Chroma-specific APIs.
It exposes both a low-level `ChromaVectorStore` class and a high-level
`store_embeddings` helper that integrates LangChain + OpenAI embeddings.
"""

from dataclasses import dataclass, field
from importlib import import_module
from typing import Any
from uuid import uuid4


def _get_settings():
    """Load application settings from either supported import path."""
    for module_name in ("app.core.config", "backend.app.core.config"):
        try:
            return import_module(module_name).settings
        except ModuleNotFoundError:
            continue
    raise ModuleNotFoundError("Could not import application settings.")


settings = _get_settings()


@dataclass
class ChromaVectorStore:
    """Small adapter for Chroma read/write operations."""

    persist_dir: str = field(default_factory=lambda: settings.chroma_persist_dir)
    collection_name: str = field(default_factory=lambda: settings.chroma_collection)

    def upsert_texts(
        self,
        texts: list[str],
        metadata: list[dict[str, Any]] | None = None,
    ) -> list[str]:
        """Store texts (and optional metadata) in Chroma.

        TODO:
            - Initialize persistent Chroma client
            - Embed texts
            - Upsert ids/documents/metadatas/embeddings
        """
        _ = metadata or [{} for _ in texts]
        return [f"doc-{uuid4().hex[:12]}" for _ in texts]

    def similarity_search(self, query: str, top_k: int = 4) -> list[dict[str, Any]]:
        """Retrieve top-k relevant chunks for `query` via LangChain retriever.

        Delegates to `rag_pipeline.retriever.retrieve_answer` so all
        retrieval logic stays in one canonical place.
        """
        from rag_pipeline.retriever import retrieve_answer
        return retrieve_answer(query=query, top_k=top_k)


def store_embeddings(
    chunks: list[str],
    source_file: str = "unknown",
    collection_name: str | None = None,
    persist_dir: str | None = None,
) -> int:
    """Convert text chunks into embeddings and store them in Chroma.

    Uses LangChain's OpenAI embedding integration so the same embedding
    model can be swapped out by changing a single config value.

    Args:
        chunks:          List of text strings to embed and store.
        source_file:     Label attached to every chunk as metadata.
        collection_name: Chroma collection to upsert into (falls back to env/default).
        persist_dir:     Directory for Chroma persistence (falls back to env/default).

    Returns:
        Number of chunks successfully stored.
    """
    # Step 1: Resolve configuration from arguments or environment variables.
    resolved_collection = collection_name or settings.chroma_collection
    resolved_persist_dir = persist_dir or settings.chroma_persist_dir
    openai_api_key = settings.openai_api_key

    # Step 2: Guard against missing API key early to give a clear error message.
    if not openai_api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY is not set. Add it to your .env file."
        )

    # Step 3: Guard against an empty chunk list — nothing to store.
    if not chunks:
        return 0

    # Step 4: Import LangChain dependencies here so that import errors surface
    #         with an actionable message if the packages are not installed.
    try:
        from langchain_chroma import Chroma
        from langchain_openai import OpenAIEmbeddings
    except ImportError as exc:
        raise ImportError(
            "langchain-chroma and langchain-openai are required. "
            "Install them with: pip install langchain-chroma langchain-openai"
        ) from exc

    # Step 5: Build the OpenAI embedding model using the configured API key.
    embedding_model = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=openai_api_key,
    )

    # Step 6: Attach source-file metadata to every chunk so we can trace
    #         retrieved context back to its origin document.
    metadatas = [{"source": source_file, "chunk_index": i} for i, _ in enumerate(chunks)]

    # Step 7: Generate unique deterministic IDs so re-running ingestion on the
    #         same file overwrites existing records instead of creating duplicates.
    ids = [f"{source_file}__chunk_{i}" for i in range(len(chunks))]

    # Step 8: Initialize (or connect to) the persistent Chroma collection.
    vector_store = Chroma(
        collection_name=resolved_collection,
        embedding_function=embedding_model,
        persist_directory=resolved_persist_dir,
    )

    # Step 9: Upsert all chunks — Chroma will embed and index them automatically.
    vector_store.add_texts(
        texts=chunks,
        metadatas=metadatas,
        ids=ids,
    )

    # Step 10: Return the number of chunks stored so callers can log/verify.
    return len(chunks)

"""Main ingestion workflow.

Orchestrates loading, chunking, and indexing into Chroma.
"""

from ingestion.chunking import chunk_text
from ingestion.loaders import load_files
from vector_db.chroma_client import ChromaVectorStore


def run_ingestion(file_paths: list[str]) -> int:
    """Ingest a file batch into vector storage.

    Returns:
        Number of chunks indexed.
    """
    loaded_docs = load_files(file_paths)
    vector_store = ChromaVectorStore()

    all_chunks: list[str] = []
    all_metadata: list[dict[str, str]] = []

    for source_path, text in loaded_docs.items():
        chunks = chunk_text(text)
        all_chunks.extend(chunks)
        all_metadata.extend({"source": source_path} for _ in chunks)

    if all_chunks:
        vector_store.upsert_texts(texts=all_chunks, metadata=all_metadata)
    return len(all_chunks)

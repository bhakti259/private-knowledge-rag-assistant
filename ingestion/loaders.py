"""Input loaders for ingestion.

Keep source-specific parsing here (files, URLs, APIs, etc.).
"""

from pathlib import Path


def load_text_file(file_path: str) -> str:
    """Load UTF-8 text from a single file path.

    TODO:
        Add robust parsers for PDF/DOCX/HTML sources.
    """
    path = Path(file_path)
    return path.read_text(encoding="utf-8")


def load_files(file_paths: list[str]) -> dict[str, str]:
    """Load multiple files and return a mapping of path -> content."""
    return {file_path: load_text_file(file_path) for file_path in file_paths}

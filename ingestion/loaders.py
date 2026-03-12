"""Input loaders for ingestion.

Keep source-specific parsing here (files, URLs, APIs, etc.).
"""

from pathlib import Path


def extract_text_from_pdf(file_path: str) -> str:
    """Read a PDF file and return text extracted from all pages."""

    # Step 1: Normalize input into a Path object for reliable path operations.
    path = Path(file_path)

    # Step 2: Validate that the file exists before attempting to open it.
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    # Step 3: Ensure the function is only used with PDF files.
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file, got: {path.name}")

    # Step 4: Import PyPDF2 locally so we can provide a clear installation error.
    try:
        from PyPDF2 import PdfReader
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise ImportError(
            "PyPDF2 is required for PDF extraction. Install it with `pip install PyPDF2`."
        ) from exc

    # Step 5: Open the PDF in binary mode and initialize the PDF reader.
    with path.open("rb") as pdf_stream:
        reader = PdfReader(pdf_stream)

        # Step 6: Iterate through each page and extract text page-by-page.
        page_texts: list[str] = []
        for page in reader.pages:
            # Some pages may return None; convert those safely to empty strings.
            extracted_text = page.extract_text() or ""
            page_texts.append(extracted_text)

    # Step 7: Join all pages into one text blob and trim surrounding whitespace.
    return "\n".join(page_texts).strip()


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

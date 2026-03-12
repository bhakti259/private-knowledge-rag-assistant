"""PDF upload + ingestion endpoint module.

Provides `/upload_pdf` which:
  1. Accepts a PDF via multipart POST.
  2. Saves it to the `uploads/` folder.
  3. Extracts raw text with PyPDF2.
  4. Splits the text into overlapping chunks.
  5. Embeds and stores those chunks in Chroma via OpenAI embeddings.
"""

import asyncio
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from pydantic import BaseModel

from ingestion.loaders import extract_text_from_pdf
from ingestion.chunking import chunk_text
from vector_db.chroma_client import store_embeddings

router = APIRouter()

# Store uploaded files in a local `uploads/` folder (created on demand).
UPLOADS_DIR = Path("uploads")

# Accepted MIME types for PDF uploads.
ALLOWED_PDF_CONTENT_TYPES = {"application/pdf", "application/x-pdf"}


class UploadPdfResponse(BaseModel):
    """Response payload returned after a successful PDF upload and ingestion."""

    file_path: str
    chunks_stored: int


def _write_upload_to_disk(upload_file: UploadFile, destination: Path) -> int:
    """Copy uploaded file contents to disk using chunked writes.

    Note:
        This function is intentionally synchronous and is executed in a worker
        thread via `asyncio.to_thread(...)` to avoid blocking the event loop.
    """
    total_bytes = 0
    with destination.open("wb") as output_buffer:
        while True:
            chunk = upload_file.file.read(1024 * 1024)  # 1 MB chunks
            if not chunk:
                break
            output_buffer.write(chunk)
            total_bytes += len(chunk)
    return total_bytes


@router.post(
    "/upload_pdf",
    response_model=UploadPdfResponse,
    summary="Upload a PDF file",
)
async def upload_pdf(file: UploadFile = File(...)) -> UploadPdfResponse:
    """Accept a PDF upload, persist it under `uploads/`, and return the path."""

    # 1) Validate that an actual file name is present in the request payload.
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file was provided.",
        )

    # 2) Normalize filename to prevent directory traversal and unsafe paths.
    original_name = Path(file.filename).name
    file_extension = Path(original_name).suffix.lower()
    if file_extension != ".pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .pdf files are allowed.",
        )

    # 3) Validate MIME type when available to reduce accidental wrong uploads.
    if file.content_type and file.content_type not in ALLOWED_PDF_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid content type: {file.content_type}. Expected a PDF.",
        )

    # 4) Create uploads directory (if missing) and generate a unique file name.
    await asyncio.to_thread(UPLOADS_DIR.mkdir, parents=True, exist_ok=True)
    unique_name = f"{Path(original_name).stem}_{uuid4().hex}.pdf"
    destination = UPLOADS_DIR / unique_name

    try:
        # 5) Save file contents in a worker thread to keep this endpoint async-safe.
        bytes_written = await asyncio.to_thread(_write_upload_to_disk, file, destination)

        # 6) Reject empty uploads and clean up any created placeholder file.
        if bytes_written == 0:
            await asyncio.to_thread(destination.unlink, missing_ok=True)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded PDF is empty.",
            )

    except HTTPException:
        # Re-raise known validation/business errors as-is.
        raise
    except Exception as exc:
        # 7) Best-effort cleanup of partial files and return a safe server error.
        if destination.exists():
            await asyncio.to_thread(destination.unlink)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save uploaded PDF.",
        ) from exc
    finally:
        # 8) Close the temporary uploaded file handle in all code paths.
        await file.close()

    # 9) Extract raw text from the saved PDF using PyPDF2.
    try:
        raw_text = await asyncio.to_thread(extract_text_from_pdf, str(destination))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Could not extract text from PDF: {exc}",
        ) from exc

    # 10) Split the extracted text into overlapping chunks for retrieval quality.
    chunks = await asyncio.to_thread(chunk_text, raw_text)

    # 11) Embed each chunk via OpenAI and upsert into Chroma.
    #     Pass the saved file path as source metadata so chunks are traceable.
    try:
        chunks_stored = await asyncio.to_thread(
            store_embeddings,
            chunks,
            str(destination),  # source_file label attached to every chunk
        )
    except EnvironmentError as exc:
        # Missing API key — surface as a clear 500 so the operator can fix config.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to store embeddings: {exc}",
        ) from exc

    # 12) Return the saved path and how many chunks were indexed.
    return UploadPdfResponse(
        file_path=str(destination.resolve()),
        chunks_stored=chunks_stored,
    )

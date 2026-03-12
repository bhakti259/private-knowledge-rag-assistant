"""Convenience launcher for local development.

Run from the `backend/` directory:
    python run.py

This is equivalent to:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Unlike a plain `uvicorn ... --reload` started from `backend/`, this launcher
also watches sibling folders like `ingestion/`, `rag_pipeline/`, and
`vector_db/` so edits there trigger a restart too.
"""

from pathlib import Path

import uvicorn


REPO_ROOT = Path(__file__).resolve().parents[1]
RELOAD_DIRS = [
    REPO_ROOT / "backend",
    REPO_ROOT / "ingestion",
    REPO_ROOT / "rag_pipeline",
    REPO_ROOT / "vector_db",
]

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(path) for path in RELOAD_DIRS],
    )

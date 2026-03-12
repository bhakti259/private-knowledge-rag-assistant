"""Health-check endpoints for service availability and smoke checks."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Backend health check")
def health_check() -> dict[str, str]:
    """Return basic runtime status used by local/dev monitoring."""
    return {"status": "ok", "service": "private-ai-knowledge-agent"}

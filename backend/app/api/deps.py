"""Dependency providers used by FastAPI route handlers.

Each dependency is isolated so services can be swapped or mocked in tests.
"""

from fastapi import Depends

from app.services.agent_service import AgentService
from app.services.ollama_client import OllamaClient
from app.services.rag_service import RagService


def get_ollama_client() -> OllamaClient:
    """Provide a local Ollama API client instance."""
    return OllamaClient()


def get_rag_service() -> RagService:
    """Provide retrieval and context assembly service."""
    return RagService()


def get_agent_service(
    ollama_client: OllamaClient = Depends(get_ollama_client),
    rag_service: RagService = Depends(get_rag_service),
) -> AgentService:
    """Provide orchestration service that coordinates agents + RAG + LLM.

    Note:
        FastAPI dependency overrides can replace these defaults in tests.
    """
    return AgentService(
        ollama_client=ollama_client,
        rag_service=rag_service,
    )

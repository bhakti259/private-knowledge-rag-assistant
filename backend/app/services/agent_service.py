"""Agent orchestration service.

Acts as a single entry point for route handlers to invoke the agent workflow.
"""

from app.services.ollama_client import OllamaClient
from app.services.rag_service import RagService

try:
    from agents.graph import build_graph
except Exception:  # pragma: no cover - safe skeleton fallback
    build_graph = None  # type: ignore[assignment]


class AgentService:
    """Coordinates LangGraph, retrieval, and LLM generation for responses."""

    def __init__(self, ollama_client: OllamaClient, rag_service: RagService) -> None:
        self.ollama_client = ollama_client
        self.rag_service = rag_service
        self.graph = build_graph() if callable(build_graph) else None

    async def run(self, query: str, session_id: str | None = None) -> str:
        """Run one request through the agent flow.

        TODO:
            Replace placeholder with `self.graph.invoke(...)` once nodes are complete.
        """
        context_chunks = self.rag_service.retrieve(query=query)
        prompt = (
            "You are a private-knowledge assistant. "
            f"Session={session_id or 'default'}\n"
            f"Context chunks={len(context_chunks)}\n"
            f"Question={query}"
        )
        return await self.ollama_client.generate(prompt)

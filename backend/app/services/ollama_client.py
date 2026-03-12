"""Small wrapper for local Ollama model interactions.

Replace the placeholder logic with real HTTP calls to `/api/generate` or `/api/chat`.
"""

from dataclasses import dataclass

from app.core.config import settings


@dataclass
class OllamaClient:
    """Client facade for local Ollama runtime."""

    base_url: str = settings.ollama_base_url
    model: str = settings.ollama_model

    async def generate(self, prompt: str) -> str:
        """Generate text from the configured Ollama model.

        TODO:
            - Add an async HTTP client (e.g., `httpx.AsyncClient`)
            - Call Ollama with streaming/non-streaming options
            - Handle model and connection errors robustly
        """
        return f"[placeholder:{self.model}] {prompt[:160]}"

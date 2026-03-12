"""Environment-driven runtime settings.

Centralized settings keep config concerns separate from business logic.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


REPO_ROOT = Path(__file__).resolve().parents[3]
ROOT_ENV_FILE = REPO_ROOT / ".env"


class Settings(BaseSettings):
    """Typed configuration loaded from environment variables."""

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    embedding_model: str = "nomic-embed-text"

    # OpenAI API key used for embeddings (text-embedding-3-small).
    openai_api_key: str = ""

    chroma_persist_dir: str = "./vector_db/chroma_store"
    chroma_collection: str = "private_knowledge_base"

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    frontend_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        # Always load the repo-root `.env`, even when the server is started
        # from `backend/`.
        env_file=str(ROOT_ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        """Expose CORS origins in list form for FastAPI middleware."""
        return [self.frontend_origin]


settings = Settings()

"""Environment-driven runtime settings.

Centralized settings keep config concerns separate from business logic.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed configuration loaded from environment variables."""

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    embedding_model: str = "nomic-embed-text"

    chroma_persist_dir: str = "./vector_db/chroma_store"
    chroma_collection: str = "private_knowledge_base"

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    frontend_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        """Expose CORS origins in list form for FastAPI middleware."""
        return [self.frontend_origin]


settings = Settings()

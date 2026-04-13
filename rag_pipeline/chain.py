"""Prompt composition and answer generation utilities for RAG answers."""

from importlib import import_module
from typing import Any


def _get_settings():
    """Load application settings from either supported import path."""
    for module_name in ("app.core.config", "backend.app.core.config"):
        try:
            return import_module(module_name).settings
        except ModuleNotFoundError:
            continue
    raise ModuleNotFoundError("Could not import application settings.")


def build_rag_prompt(query: str, contexts: list[dict[str, Any]]) -> str:
    """Build a single prompt string from query + retrieved context."""
    context_block = "\n\n".join(
        f"- {item.get('text', '')}" for item in contexts if item.get("text")
    )
    if not context_block:
        context_block = "No relevant context retrieved."

    return (
        "You are a private knowledge assistant. Use context when relevant.\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question:\n{query}\n\n"
        "Answer clearly and mention uncertainty when context is insufficient."
    )


def generate_answer(query: str, contexts: list[dict[str, Any]]) -> str:
    """Generate a natural-language answer from retrieved chunks using OpenAI.

    Args:
        query:    The user's question.
        contexts: List of chunk dicts returned by the retriever.

    Returns:
        A synthesized answer string.
    """
    from langchain_openai import ChatOpenAI

    settings = _get_settings()

    if not settings.openai_api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY is not set. Add it to your .env file."
        )

    prompt = build_rag_prompt(query, contexts)

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=settings.openai_api_key,
        temperature=0.3,
    )

    response = llm.invoke(prompt)
    return response.content

"""Prompt composition utilities for RAG answers."""

from typing import Any


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

"""Typed state object shared across LangGraph nodes."""

from typing import Any, Literal, TypedDict


class AgentState(TypedDict, total=False):
    """State contract flowing between nodes in the LangGraph workflow."""

    query: str
    session_id: str | None
    route: Literal["rag", "fallback"]
    retrieved_chunks: list[dict[str, Any]]
    answer: str

"""Fallback node.

Handles cases where retrieval is not suitable or query is invalid/empty.
"""

from agents.state import AgentState


def fallback_node(state: AgentState) -> AgentState:
    """Return a safe default assistant response."""
    answer = "Please provide a question so I can search your private knowledge base."
    return {**state, "answer": answer}

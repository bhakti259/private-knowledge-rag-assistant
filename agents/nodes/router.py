"""Routing node.

Determines whether a request should go through retrieval or fallback handling.
"""

from agents.state import AgentState


def router_node(state: AgentState) -> AgentState:
    """Route requests based on query availability/quality.

    TODO:
        Upgrade with intent classification and confidence scoring.
    """
    query = (state.get("query") or "").strip()
    route = "rag" if query else "fallback"
    return {**state, "route": route}

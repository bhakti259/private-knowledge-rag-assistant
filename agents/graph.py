"""Graph assembly for LangGraph-based orchestration.

This module wires node transitions while keeping node logic isolated.
"""

from agents.nodes.fallback import fallback_node
from agents.nodes.generate import generate_node
from agents.nodes.retrieve import retrieve_node
from agents.nodes.router import router_node
from agents.state import AgentState

try:
    from langgraph.graph import END, StateGraph

    LANGGRAPH_AVAILABLE = True
except Exception:  # pragma: no cover - optional during early scaffolding
    END = "END"
    StateGraph = object  # type: ignore[assignment]
    LANGGRAPH_AVAILABLE = False


def _select_route(state: AgentState) -> str:
    """Select next edge key from current state."""
    return state.get("route", "fallback")


def build_graph():
    """Create and compile the LangGraph workflow.

    Returns:
        Compiled graph object, or `None` if LangGraph is unavailable.
    """
    if not LANGGRAPH_AVAILABLE:
        return None

    workflow = StateGraph(AgentState)
    workflow.add_node("router", router_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("fallback", fallback_node)

    workflow.set_entry_point("router")
    workflow.add_conditional_edges(
        "router",
        _select_route,
        {
            "rag": "retrieve",
            "fallback": "fallback",
        },
    )
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)
    workflow.add_edge("fallback", END)
    return workflow.compile()

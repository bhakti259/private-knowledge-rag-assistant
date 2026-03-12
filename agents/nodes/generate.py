"""Generation node.

Builds a response from query + retrieved context.
"""

from agents.state import AgentState


def generate_node(state: AgentState) -> AgentState:
    """Create a placeholder answer using current state.

    TODO:
        Call Ollama through a shared client and store citations.
    """
    chunk_count = len(state.get("retrieved_chunks", []))
    answer = f"Placeholder answer generated from {chunk_count} retrieved chunk(s)."
    return {**state, "answer": answer}

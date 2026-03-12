"""Retrieval node.

Populates `retrieved_chunks` in state using the configured vector search stack.
"""

from agents.state import AgentState


def retrieve_node(state: AgentState) -> AgentState:
    """Attach placeholder chunks to state.

    TODO:
        Integrate with `rag_pipeline.retriever.retrieve_chunks(...)`.
    """
    retrieved_chunks = [
        {
            "id": "chunk-001",
            "text": "Placeholder context from vector store.",
            "metadata": {"source": "todo.md"},
        }
    ]
    return {**state, "retrieved_chunks": retrieved_chunks}

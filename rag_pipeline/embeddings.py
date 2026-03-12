"""Embedding helpers.

Replace placeholder vectors with calls to your chosen embedding model.
"""


def embed_texts(texts: list[str], dimension: int = 384) -> list[list[float]]:
    """Return placeholder embeddings for supplied texts.

    TODO:
        Call Ollama embeddings or another local embedding model.
    """
    return [[0.0] * dimension for _ in texts]

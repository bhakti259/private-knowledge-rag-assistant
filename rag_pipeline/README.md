# RAG Pipeline Module

This module transforms user queries into retrieval + prompt inputs for generation.

## Responsibilities

- Generate or request embeddings (`embeddings.py`)
- Retrieve context chunks (`retriever.py`)
- Compose final LLM prompt (`chain.py`)

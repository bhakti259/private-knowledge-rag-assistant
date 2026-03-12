# Vector DB Module (Chroma)

This module encapsulates all direct access to Chroma.

## Responsibilities

- Initialize/manage Chroma collections
- Upsert chunk embeddings + metadata
- Run similarity searches for retrieval

Keeping this isolated makes it easy to replace Chroma later if needed.

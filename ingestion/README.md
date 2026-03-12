# Ingestion Module

This module handles converting raw source documents into vector-store-ready chunks.

## Responsibilities

- Load raw documents from supported sources (`loaders.py`)
- Split text into chunks (`chunking.py`)
- Push chunks into vector DB (`pipeline.py`)

Implement this module first to populate your knowledge base before chat.

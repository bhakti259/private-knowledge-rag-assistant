# Backend (FastAPI)

This module exposes the HTTP API for chat and ingestion.

## Responsibilities

- Route incoming requests (`app/api/routes`)
- Validate payloads (`app/schemas`)
- Orchestrate services (`app/services`)
- Read environment configuration (`app/core/config.py`)

## Entry Point

- `app/main.py` builds and configures the FastAPI application.

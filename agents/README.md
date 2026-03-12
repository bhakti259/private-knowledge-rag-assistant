# Agents (LangGraph)

This package defines the agent workflow as composable graph nodes.

## Responsibilities

- Shared state schema (`state.py`)
- Graph construction and routing (`graph.py`)
- Individual node handlers (`nodes/*.py`)

Keep each node single-purpose so it can be independently tested.

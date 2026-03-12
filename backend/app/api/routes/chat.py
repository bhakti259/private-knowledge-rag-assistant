"""Chat endpoint module.

Converts user prompts into agent-service calls and structured API responses.
"""

from fastapi import APIRouter, Depends

from app.api.deps import get_agent_service
from app.schemas.chat import ChatRequest, ChatResponse, SourceChunk
from app.services.agent_service import AgentService

router = APIRouter()


@router.post("/", response_model=ChatResponse, summary="Ask the knowledge agent")
async def chat(
    payload: ChatRequest,
    agent_service: AgentService = Depends(get_agent_service),
) -> ChatResponse:
    """Handle a user message and return an answer (plus optional sources)."""
    answer_text = await agent_service.run(
        query=payload.message,
        session_id=payload.session_id,
    )

    # TODO: Return real source metadata once retriever wiring is complete.
    return ChatResponse(answer=answer_text, sources=[SourceChunk(id="placeholder")])

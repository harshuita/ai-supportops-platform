
from fastapi import APIRouter, Depends, HTTPException

from app.agent.agent import ask_agent
from app.core.dependencies import get_current_user
from app.schemas.agent import AgentChatRequest, AgentChatResponse

router = APIRouter(
    prefix="/agent",
    tags=["Agent"]
)
@router.post("/chat",response_model=AgentChatResponse)
def chat_with_agent(request: AgentChatRequest, current_user=Depends(get_current_user)):
    """
    Endpoint to chat with the agent.
    """
    try:
        answer = ask_agent(request.question)
        return AgentChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
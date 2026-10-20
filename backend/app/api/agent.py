
from fastapi import APIRouter, Depends, HTTPException

from app.agent.agent import ask_agent
from app.core.dependencies import get_current_user
from app.schemas.agent import AgentChatRequest, AgentChatResponse

router = APIRouter(
    prefix="/agent",
    tags=["Agent"]
)

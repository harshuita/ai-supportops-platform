
from pydantic import BaseModel, Field


class AgentChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class AgentChatResponse(BaseModel):
    answer: str

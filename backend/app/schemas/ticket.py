
from datetime import datetime

from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    customer_id: int = Field(gt=0)
    order_id: int | None = Field(default=None, gt=0)
    subject: str = Field(min_length=3, max_length=255)
    message: str = Field(min_length=5, max_length=2000)


class TicketResponse(BaseModel):
    id: int
    customer_id: int
    order_id: int | None
    subject: str
    message: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TicketStatusUpdate(BaseModel):
    status: str = Field(
        pattern="^(open|in_progress|resolved|closed)$"
    )

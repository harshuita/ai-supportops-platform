from pydantic import BaseModel, Field
from typing import Literal
from pydantic import BaseModel

class OrderCreate(BaseModel):
    customer_id: int = Field(gt=0)
    product_name: str = Field(min_length=1, max_length=150)
    quantity: int = Field(gt=0)


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    product_name: str
    quantity: int
    status: str

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: Literal["created", "processing", "shipped", "cancelled"]
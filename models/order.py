from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class OrderItem(BaseModel):
    part_id: str
    quantity: int = Field(gt=0)

class Order(BaseModel):
    id: Optional[str] = Field(default=None)
    client_id: str
    date: datetime = Field(default_factory=datetime.utcnow)
    items: List[OrderItem]
    subtotal: float = Field(gt=0)
    taxes: float = Field(ge=0)
    discount: float = Field(ge=0)
    total: float = Field(gt=0)
    status: Optional[str] = Field(default="reserved")

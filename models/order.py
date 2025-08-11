from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class OrderItem(BaseModel):
    part_id: str
    quantity: int = Field(..., gt=0)

class Order(BaseModel):
    id: Optional[str] = None
    user_id: str
    date: datetime = Field(default_factory=datetime.utcnow)
    items: List[OrderItem]
    subtotal: float
    taxes: float = 0.0
    discount: float = 0.0
    total: float

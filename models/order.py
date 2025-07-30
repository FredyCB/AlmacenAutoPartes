from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class OrderItem(BaseModel):
    id_part: str
    quantity: int = Field(gt=0)

class Order(BaseModel):
    id: Optional[str] = Field(default=None)
    id_user: str
    date: datetime = Field(default_factory=datetime.utcnow)
    items: List[OrderItem]
    subtotal: float = Field(gt=0)
    taxes: float = Field(ge=0)
    discount: float = Field(ge=0)
    total: float = Field(gt=0)
from pydantic import BaseModel, Field
from typing import Optional

class Inventory(BaseModel):
    id: Optional[str] = None
    part_id: str = Field(...)
    quantity: int = Field(..., ge=0)
    location: str = Field(default="")

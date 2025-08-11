from pydantic import BaseModel, Field
from typing import Optional, List

class Part(BaseModel):
    id: Optional[str] = None
    name: str = Field(...)
    description: str = Field(...)
    price: float = Field(..., gt=0)
    compatible_vehicles: List[str] = Field(default_factory=list)
    active: bool = True

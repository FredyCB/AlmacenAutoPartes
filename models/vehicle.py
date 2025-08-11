from pydantic import BaseModel, Field
from typing import Optional

class Vehicle(BaseModel):
    id: Optional[str] = None
    brand: str = Field(...)
    model: str = Field(...)
    year: int = Field(..., ge=1900, le=2100)
    active: bool = True

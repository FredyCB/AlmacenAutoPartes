from pydantic import BaseModel, Field
from typing import Optional

class Vehicle(BaseModel):
    id: Optional[str] = Field(default=None)
    brand: str
    model: str
    year: int = Field(ge=1900, le=2100)
    active: bool = Field(default=True)

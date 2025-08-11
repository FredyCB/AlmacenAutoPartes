from pydantic import BaseModel, Field
from typing import Optional

class VehiclePart(BaseModel):
    id: Optional[str] = None
    vehicle_id: str = Field(...)
    part_id: str = Field(...)
    notes: Optional[str] = None

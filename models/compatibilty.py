from pydantic import BaseModel, Field
from typing import Optional

class Compatibility(BaseModel):
    id: Optional[str] = Field(default=None)
    id_part: str
    id_vehicle: str

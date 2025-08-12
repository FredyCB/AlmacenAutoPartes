from pydantic import BaseModel, Field
from typing import Optional, List

class Part(BaseModel):
    id: Optional[str] = Field(default=None)
    name: str = Field(description="Nombre de la pieza")
    description: str = Field(description="Descripción")
    price: float = Field(gt=0)
    compatible_vehicles: List[str] = Field(default=[], description="IDs de vehículos compatibles")
    active: bool = Field(default=True)

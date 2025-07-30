from pydantic import BaseModel, Field
from typing import Optional

class Inventory(BaseModel):
    id: Optional[str] = Field(default=None)
    id_part: str = Field(description="ID de la pieza")
    id_provider: str = Field(description="ID del proveedor")
    stock: int = Field(ge=0)

from pydantic import BaseModel, Field
from typing import Optional

class Provider(BaseModel):
    id: Optional[str] = Field(default=None)
    name: str = Field(..., description="Nombre del proveedor")
    contact_email: str
    phone: str
    active: bool = Field(default=True)

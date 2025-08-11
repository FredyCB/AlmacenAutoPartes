from pydantic import BaseModel, Field
from typing import Optional

class Provider(BaseModel):
    id: Optional[str] = None
    name: str = Field(...)
    contact_email: str = Field(...)
    phone: str = Field(...)
    active: bool = True

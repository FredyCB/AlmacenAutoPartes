from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class User(BaseModel):
    id: Optional[str] = Field(default=None, description="ID MongoDB (string)")
    name: str = Field(..., description="Nombres")
    lastname: str = Field(..., description="Apellidos")
    email: str = Field(..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    active: bool = Field(default=True)
    admin: bool = Field(default=False)
    password: Optional[str] = Field(None, min_length=8, max_length=64, description="Solo para creación, no se guarda en DB")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if v is None:
            return v
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contraseña debe contener al menos una mayúscula")
        if not re.search(r"\d", v):
            raise ValueError("La contraseña debe contener al menos un número")
        if not re.search(r"[@$!%*?&]", v):
            raise ValueError("La contraseña debe contener al menos un carácter especial")
        return v
